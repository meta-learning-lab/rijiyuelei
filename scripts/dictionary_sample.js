// 在已登录 bjzs.vdict.com.cn 的页面开发者工具中执行。
// 小样本验证工具；不包含、提取或保存登录凭据。
(async () => {
  const words = ['挎', '奔', '规矩', '不料', '衣裳'];
  const output = [];
  const readJson = async (url) => {
    const response = await fetch(url, { credentials: 'same-origin' });
    if (!response.ok) throw new Error(`HTTP ${response.status}`);
    const data = await response.json();
    if (data.code !== 200) throw new Error(data.msg || `code ${data.code}`);
    return data;
  };
  for (const word of words) {
    try {
      const search = await readJson(`/api/front/search/turnPage?input=${encodeURIComponent(word)}&pageNo=1`);
      const book = search.books?.find((item) => item.bookId === 2);
      const text = (html) => new DOMParser().parseFromString(html, 'text/html').body.textContent.trim();
      const matches = book?.items?.filter((item) => text(item.name) === word) || [];
      if (!matches.length) { output.push({ word, error: '首页未找到精确词条' }); continue; }
      const seen = new Set();
      for (const match of matches) {
        const first = await readJson(`/api/front/item/detail/${encodeURIComponent(match.uuid)}`);
        const variants = first.phoneticTranscription?.length ? first.phoneticTranscription : [{ uuid: match.uuid, pronunciation: match.phoneticTranscription }];
        for (const variant of variants) {
          if (seen.has(variant.uuid)) continue;
          seen.add(variant.uuid);
          const detail = variant.uuid === match.uuid ? first : await readJson(`/api/front/item/detail/${encodeURIComponent(variant.uuid)}`);
          if (!detail.info?.infoHtml || !detail.fonts?.all) throw new Error('缺少正文或字体信息');
          output.push({ word, uuid: variant.uuid, pinyin: variant.pronunciation, html: detail.info.infoHtml, fonts: detail.fonts.all });
        }
      }
    } catch (error) { output.push({ word, error: String(error) }); }
  }
  return output;
})()
