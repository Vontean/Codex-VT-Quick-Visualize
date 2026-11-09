// 标题与数据图例共用一次宽度观察；绘制及语义留在各图型。
function alignChartPresentation(root){
 const selector='.radar-legend,.xy-key,.legend,.quick-radar-legend';
 function title(){
  if(root.classList.contains('qv-mermaid')&&root.dataset.state!=='enhanced')return;
  const heading=root.querySelector('h3');if(!heading)return;
  const line=parseFloat(getComputedStyle(heading).lineHeight);
  heading.toggleAttribute('data-title-wrapped',!!heading.offsetHeight&&heading.scrollHeight>line*1.5);
 }
 function legend(element){
  if(element.hidden||!element.children.length)return;
  element.removeAttribute('data-legend-stacked');
  const items=[...element.children].filter(item=>item.offsetParent);
  if(new Set(items.map(item=>item.offsetTop)).size<2)return;
  for(const item of items){
   item.title||=item.textContent.trim();
   for(const text of [...item.childNodes])if(text.nodeType===3&&text.textContent.trim()){
    const span=document.createElement('span');span.className='qv-legend-text';text.replaceWith(span);span.append(text);
   }
   for(const span of item.querySelectorAll('span'))if(!span.children.length&&span.textContent.trim()&&!span.classList.contains('percent'))span.classList.add('qv-legend-text');
  }
  element.setAttribute('data-legend-stacked','');
 }
 function refresh(){title();root.querySelectorAll(selector).forEach(legend);}
 refresh();
 if(root.__qvAlignmentObserver)return;
 let width=root.clientWidth;
 root.__qvAlignmentObserver=new ResizeObserver(()=>{
  if(root.clientWidth===width)return;
  width=root.clientWidth;requestAnimationFrame(refresh);
 });
 root.__qvAlignmentObserver.observe(root);
}
