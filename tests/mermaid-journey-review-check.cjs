const fs=require('node:fs'),path=require('node:path');
const {chromium}=require('playwright');
const check=eval('('+fs.readFileSync(path.join(__dirname,'mermaid-journey-design-check.js'),'utf8')+')');
(async()=>{
 const browser=await chromium.launch();
 try{
  const page=await browser.newPage();let count=0;
  for(const [fixture,preview] of [
   ['adapted-journey.mmd','journey-redesign-preview.html'],
   ['journey-resize-stress.mmd','journey-stress-preview.html'],
   ['journey-long-final-actor.mmd','journey-long-final-actor-preview.html']
  ])count+=(await check(page,fs.readFileSync(path.join(__dirname,'fixtures/mermaid',fixture),'utf8'),preview)).length;
  console.log('PASS Journey design:',count,'theme/sample cases');
 }finally{await browser.close();}
})().catch(error=>{console.error(error);process.exitCode=1;});
