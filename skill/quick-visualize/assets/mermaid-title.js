// 使用 Mermaid 相同的 JSON_SCHEMA 读取完整 YAML；只在含 frontmatter 时加载。
async function readMermaidTitle(source) {
 const match=source.replace(/\r\n?/g,'\n').match(/^-{3}\s*[\n\r](.*?)[\n\r]-{3}\s*[\n\r]+/s);
 if(!match)return '';
 const {load,JSON_SCHEMA}=await import('https://cdn.jsdelivr.net/npm/js-yaml@4.1.1/+esm');
 const metadata=load(match[1],{schema:JSON_SCHEMA});
 return metadata&&typeof metadata==='object'&&!Array.isArray(metadata)&&metadata.title?String(metadata.title):'';
}
