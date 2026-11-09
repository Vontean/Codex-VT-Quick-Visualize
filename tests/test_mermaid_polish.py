import json
import subprocess
import unittest
from pathlib import Path

ASSETS = Path(__file__).resolve().parents[1] / 'skill/quick-visualize/assets'


class MermaidPolishTests(unittest.TestCase):
    def node(self, assets, code):
        source = '\n'.join((ASSETS / file).read_text() for file in assets)
        result = subprocess.run(['node', '-e', source + '\n' + code], text=True, capture_output=True, check=True)
        return json.loads(result.stdout)

    def test_nearby_beats_empty_remote_corner(self):
        result = self.node(['chart-detail-position.js'], '''
console.log(JSON.stringify(nearbyRadarDetails([
 {distance:0,pointer:1,area:0},{distance:16,pointer:0,area:80},
 {distance:32,pointer:0,area:20},{distance:240,pointer:0,area:0}
]).map(c=>c.distance)));''')
        self.assertEqual(result, [16, 32])

    def test_constrained_edge_uses_nearest_plus_sixteen(self):
        result = self.node(['chart-detail-position.js'], '''
console.log(JSON.stringify(nearbyRadarDetails([
 {distance:6,coversPointer:1},{distance:50,coversPointer:0},
 {distance:66,coversPointer:0},{distance:67,coversPointer:0}
]).map(c=>c.distance)));''')
        self.assertEqual(result, [50, 66])

    def test_motion_batch_scales_delay_and_duration_without_patching_prototype(self):
        result = self.node(['chart-motion.js'], '''
const animations=[];const element={animate(frames,timing){
 const effect={getTiming:()=>timing,updateTiming:next=>Object.assign(timing,next)};
 const animation={effect,frames};animations.push(animation);return animation;
}};
animateMermaidEntry(element,[{transform:'scale(.08)'},{transform:'scale(1)'}],{duration:650,delay:1800});
animateMermaidEntry(element,[{opacity:0},{opacity:1}],{duration:240,delay:600});
queueMicrotask(()=>console.log(JSON.stringify(animations.map(a=>({
 ...a.effect.getTiming(),frames:a.frames
})))));''')
        self.assertAlmostEqual(max(x['delay'] + x['duration'] for x in result), 1200)
        self.assertEqual(result[0]['frames'][0]['transform'], 'scale(0.92)')
        self.assertAlmostEqual(result[0]['delay'] / result[0]['duration'], 1800 / 650)
        self.assertEqual(result[0]['easing'], 'cubic-bezier(.23,1,.32,1)')

    def test_git_model_preserves_merge_parents_and_tags(self):
        result = self.node(['mermaid-git.js'], '''
const hasRichMermaidLabel=s=>/<[^>]+>/.test(s);
const db={getBranchesAsObjArray:()=>[{name:'main'},{name:'design'}],getCommits:()=>new Map([
 ['merge',{id:'merge',seq:3,type:3,branch:'main',parents:['base','draft'],tags:['v1']}],
 ['base',{id:'base',seq:1,type:0,branch:'main',parents:[]}],
 ['draft',{id:'draft',seq:2,type:0,branch:'design',parents:['base']}]
])};console.log(JSON.stringify(readMermaidGitModel(db).data));''')
        self.assertEqual([c['id'] for c in result['commits']], ['base', 'draft', 'merge'])
        self.assertEqual(result['commits'][-1]['parents'], ['base', 'draft'])
        self.assertEqual(result['commits'][-1]['tags'], ['v1'])


if __name__ == '__main__':
    unittest.main()
