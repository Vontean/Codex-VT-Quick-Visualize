import json
import subprocess
import unittest
from pathlib import Path

SCRIPT = (Path(__file__).parents[1] / 'skill/quick-visualize/assets/mermaid-navigation.js').read_text()


class MermaidNavigationTests(unittest.TestCase):
    def project(self, model, scope=None):
        script = SCRIPT + '\nconst model=' + json.dumps(model) + ';const before=JSON.stringify(model);'
        script += 'const view=mermaidScopeView(model,' + json.dumps(scope) + ');'
        script += 'if(before!==JSON.stringify(model))throw Error("mutated original model");console.log(JSON.stringify(view));'
        result = subprocess.run(['node', '-e', script], text=True, capture_output=True, check=True)
        return json.loads(result.stdout)

    def fixture(self):
        return {'direction':'LR', 'groups':[{'id':'app','name':'App'}, {'id':'api','name':'API','parent':'app'}, {'id':'data','name':'Data'}],
                'nodes':[{'id':'web','name':'Web'}, {'id':'a','name':'A','parent':'api'}, {'id':'b','name':'B','parent':'api'}, {'id':'db','name':'DB','parent':'data'}],
                'edges':[{'from':'web','to':'a','arrow':True}, {'from':'web','to':'b','arrow':True}, {'from':'a','to':'b','arrow':True}, {'from':'b','to':'db','arrow':True}, {'from':'a','to':'a','arrow':True}]}

    def test_overview_counts_and_aggregation(self):
        view=self.project(self.fixture())
        self.assertEqual({n['id'] for n in view['nodes']}, {'app','data','web'})
        edge=next(e for e in view['edges'] if e['from']=='web')
        self.assertEqual(edge['members'], [0,1])
        self.assertEqual(edge['bundleCount'], 2)
        self.assertEqual(next(n for n in view['nodes'] if n['id']=='app')['count'], 2)

    def test_drill_keeps_external_context_and_leaf_self_loop(self):
        view=self.project(self.fixture(),'api')
        self.assertEqual({n['id'] for n in view['nodes']}, {'a','b','qv-external:web','qv-external:data'})
        self.assertEqual(len(view['edges']),5)
        self.assertTrue(any(e['from']==e['to']=='a' for e in view['edges']))
        self.assertEqual(next(n for n in view['nodes'] if n['id']=='qv-external:data')['targetGroup'],'data')

    def test_nested_group_is_a_drillable_child(self):
        view=self.project(self.fixture(),'app')
        node=next(n for n in view['nodes'] if n['id']=='api')
        self.assertTrue(node['groupCard'])
        self.assertEqual(node['targetGroup'],'api')

    def test_distinct_semantics_are_not_merged(self):
        model=self.fixture()
        model['edges'] += [{'from':'web','to':'b','arrow':True,'async':True}, {'from':'web','to':'b','arrow':True,'label':'audit'}, {'from':'a','to':'web','arrow':True}]
        view=self.project(model)
        incoming=[e for e in view['edges'] if e['from']=='web']
        self.assertEqual(len(incoming),3)
        self.assertTrue(any(e['from']=='app' and e['to']=='web' for e in view['edges']))

    def test_group_endpoint_remains_visible_as_boundary_context(self):
        model=self.fixture();model['edges'].append({'from':'api','to':'b','arrow':True})
        view=self.project(model,'api')
        boundary=next(n for n in view['nodes'] if n['id']=='qv-external:api')
        self.assertTrue(boundary['external'])
        self.assertEqual(boundary['targetGroup'],'app')

    def test_preview_preserves_membership_and_real_internal_edges(self):
        view=self.project(self.fixture())
        preview=next(n for n in view['nodes'] if n['id']=='app')['preview']
        self.assertEqual([r['id'] for r in preview['rows']], ['api','a','b'])
        self.assertEqual([(e['from'],e['to']) for e in preview['edges']], [('a','b')])
        self.assertEqual(preview['remaining'], 0)

    def test_large_preview_reports_omitted_members(self):
        model=self.fixture()
        model['nodes'] += [{'id':str(i),'name':str(i),'parent':'api'} for i in range(12)]
        preview=next(n for n in self.project(model)['nodes'] if n['id']=='app')['preview']
        self.assertEqual(len([r for r in preview['rows'] if not r.get('heading')]), 8)
        self.assertEqual(preview['remaining'], 6)

    def test_scope_keeps_all_internal_nodes_including_disconnected(self):
        model=self.fixture();model['nodes'].append({'id':'isolated','name':'Isolated','parent':'api'})
        view=self.project(model,'api')
        self.assertTrue({'a','b','isolated'}.issubset({n['id'] for n in view['nodes']}))
        self.assertEqual(len(view['edges']),5)
