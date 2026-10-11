import json
import subprocess
import unittest
from pathlib import Path


class SequenceModelTests(unittest.TestCase):
    def test_numbering_and_semantic_fallback(self):
        source = Path(__file__).resolve().parents[1] / 'skill/quick-visualize/assets/mermaid-sequence-model.js'
        # DB 记录形状来自固定 Mermaid 11.12 的真实 parser probe；浏览器另测布局与交互。
        script = source.read_text() + r'''
const hasRichMermaidLabel=value=>/<[^>]+>/.test(String(value||''));
let actors=new Map([['A',{description:'编辑者',type:'actor',links:{},properties:{}}],['B',{description:'服务',type:'participant',links:{},properties:{}}]]),boxes=new Map(),messages=[];
const mermaid={mermaidAPI:{getDiagramFromText:async()=>({db:{getActors:()=>actors,getMessages:()=>messages,getBoxes:()=>boxes}})}};
(async()=>{
 const run=()=>readMermaidSequenceModel(mermaid,'fixture');
 const msg=()=>({type:0,from:'A',to:'B',message:'保存'});
 messages=[{type:26,message:{visible:true}},msg(),{type:26,message:{visible:false}},msg(),{type:26,message:{visible:true,start:10,step:5}},msg(),{type:2,message:'说明'},msg()];
 const normal=await run(), numbers=normal.data.messages.filter(m=>m.type===0).map(m=>m.number??null);
 const reasons=[];
 messages=[{type:22,message:'源码指定颜色'}];reasons.push(!!(await run()).reason);
 messages=[msg()];boxes.set('box',{name:'组织分组'});reasons.push(!!(await run()).reason);boxes.clear();
 actors.get('A').links={docs:'https://example.com'};reasons.push(!!(await run()).reason);actors.get('A').links={};
 actors.get('A').type='database';reasons.push(!!(await run()).reason);actors.get('A').type='actor';
 messages=[{...msg(),message:'<b>富文本</b>'}];reasons.push(!!(await run()).reason);
 let unknown=false;messages=[msg()];try{await readMermaidSequenceModel(mermaid,'fixture',{missing:'未存在的参与方'})}catch(e){unknown=e.message.includes('missing')}
 console.log(JSON.stringify({numbers,reasons,unknown,actor:normal.data.actors[0].type}));
})().catch(e=>{console.error(e);process.exitCode=1});
'''
        result = subprocess.run(['node', '-e', script], capture_output=True, text=True, check=True)
        data = json.loads(result.stdout)
        self.assertEqual(data['numbers'], [1, None, 10, 15])
        self.assertTrue(all(data['reasons']))
        self.assertTrue(data['unknown'])
        self.assertEqual(data['actor'], 'actor')


if __name__ == '__main__':
    unittest.main()
