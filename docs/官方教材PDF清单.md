# 官方教材 PDF 来源与校验

下载日期：2026-11-14。以下文件是使用登录后的国家中小学智慧教育平台阅读器，从其打开的官方 PDF 文档直接获取的完整原始字节，未拼接页面、重新导出或使用第三方副本。原文件地址由对应阅读器页面显示，直接访问可能因权限返回 401；访问需使用平台授权会话。

校验：12 份 PDF 的本地文件字节数均等于平台教材元数据的 size，页数均与平台阅读器显示一致；pdfinfo 和 PDFKit 均能打开，PDFKit 可加载全部页并确认页面尺寸非零；封面文本与册次一致，首尾页均可渲染，pdftotext 全文处理退出码均为 0。SHA-256 为下载文件的本地计算值，不是平台提供的原件哈希。

部分原文件在 Poppler 解析时出现 `insufficient arguments for Marked Content` 格式警告（见表），尽管首尾页渲染和 PDFKit 全页加载通过，警告仍保留，不能据此声称不存在任何格式问题。

四、五、六年级下册的平台标题未标注“根据2022年版课程标准修订”，是否为最新版未确认；其他九册的平台标题包含该标识，平台标题不等于出版印次。

| 册次及文件 | 平台条目 | 平台标题 | 阅读器页数 | 字节数 | SHA-256 | 解析警告 |
| --- | --- | --- | ---: | ---: | --- | --- |
| [一年级上册](../教材/官方PDF/一年级上册.pdf) | [平台条目](https://basic.smartedu.cn/tchMaterial/detail?contentType=assets_document&contentId=1c73b348-e8b6-47d6-84b0-6dbacbe28268&catalogType=tchMaterial&subCatalog=dzjc) | （根据2022年版课程标准修订）义务教育教科书·语文一年级上册 | 118 | 18000269 | `f8a9bba537d1925c16eced2ff79c6a2ae28804a12caf3ea362c5bbe51062013b` | 无 |
| [一年级下册](../教材/官方PDF/一年级下册.pdf) | [平台条目](https://basic.smartedu.cn/tchMaterial/detail?contentType=assets_document&contentId=b87e153f-a64c-451a-aa6c-6ed9ac7d6821&catalogType=tchMaterial&subCatalog=dzjc) | （根据2022年版课程标准修订）义务教育教科书·语文一年级下册 | 127 | 16304911 | `a503884e543a48d0a9763a42c37425665b7893897662b3f029f368ddb1b92269` | 有 |
| [二年级上册](../教材/官方PDF/二年级上册.pdf) | [平台条目](https://basic.smartedu.cn/tchMaterial/detail?contentType=assets_document&contentId=2ce8f153-7bff-4c97-b6db-9aac414fea19&catalogType=tchMaterial&subCatalog=dzjc) | （根据2022年版课程标准修订）义务教育教科书·语文二年级上册 | 126 | 18904596 | `0d1f2132731d53ff3ded1d3c1faee325f527dca1a081b9e18a6256a8d8924b9a` | 无 |
| [二年级下册](../教材/官方PDF/二年级下册.pdf) | [平台条目](https://basic.smartedu.cn/tchMaterial/detail?contentType=assets_document&contentId=0f93b83e-b3c2-4a5d-8acd-ea460ab962d4&catalogType=tchMaterial&subCatalog=dzjc) | （根据2022年版课程标准修订）义务教育教科书·语文二年级下册 | 130 | 19835956 | `86f5a17b3d3703e7a49c1f44aab3612d58590070753fbe80b6dd09953cf0fa19` | 有 |
| [三年级上册](../教材/官方PDF/三年级上册.pdf) | [平台条目](https://basic.smartedu.cn/tchMaterial/detail?contentType=assets_document&contentId=837f368e-fd4e-404a-ae3f-342d75bc0227&catalogType=tchMaterial&subCatalog=dzjc) | （根据2022年版课程标准修订）义务教育教科书·语文三年级上册 | 123 | 17598139 | `35169d6d9646a87be2ea84ea5b01de38a92774e26338d43810e8d8f22a558ac3` | 无 |
| [三年级下册](../教材/官方PDF/三年级下册.pdf) | [平台条目](https://basic.smartedu.cn/tchMaterial/detail?contentType=assets_document&contentId=8e107655-5128-451f-84e5-d158725c537b&catalogType=tchMaterial&subCatalog=dzjc) | （根据2022年版课程标准修订）义务教育教科书·语文三年级下册 | 126 | 13981443 | `af911d41b10c46908fd82610ecb0ec0f2c62fa8f609947b9748d00ab0d58e141` | 有 |
| [四年级上册](../教材/官方PDF/四年级上册.pdf) | [平台条目](https://basic.smartedu.cn/tchMaterial/detail?contentType=assets_document&contentId=5cd7e623-5c38-4602-871a-3fba8a551db2&catalogType=tchMaterial&subCatalog=dzjc) | （根据2022年版课程标准修订）义务教育教科书·语文四年级上册 | 138 | 18952430 | `a79c9ef08600c799c5fe455c27cf5c79437cbc668a86aec2cce6b15fdf9f7981` | 有 |
| [四年级下册](../教材/官方PDF/四年级下册.pdf) | [平台条目](https://basic.smartedu.cn/tchMaterial/detail?contentType=assets_document&contentId=53d6315e-5f90-42c4-904f-2d4e95fe99ed&catalogType=tchMaterial&subCatalog=dzjc) | 义务教育教科书·语文四年级下册 | 151 | 17426049 | `b5fd20a972e18a63c6e1f76ab03f9f189d25b8326ed1b5650358e2cab3e8dac1` | 有 |
| [五年级上册](../教材/官方PDF/五年级上册.pdf) | [平台条目](https://basic.smartedu.cn/tchMaterial/detail?contentType=assets_document&contentId=aabf2e4a-3ceb-4e86-8804-22c10223cc57&catalogType=tchMaterial&subCatalog=dzjc) | （根据2022年版课程标准修订）义务教育教科书·语文五年级上册 | 130 | 15981540 | `86303735a78bed9df039cfb2183c354642d93a5bd6faa2366d94e4196a95b438` | 无 |
| [五年级下册](../教材/官方PDF/五年级下册.pdf) | [平台条目](https://basic.smartedu.cn/tchMaterial/detail?contentType=assets_document&contentId=98172dc9-8fba-4da6-9fae-6a3d1166f038&catalogType=tchMaterial&subCatalog=dzjc) | 义务教育教科书·语文五年级下册 | 131 | 24193161 | `8fb0db8d5364c8118eefada554b90182ec7f6de923e43779eaa7c98efca20f47` | 有 |
| [六年级上册](../教材/官方PDF/六年级上册.pdf) | [平台条目](https://basic.smartedu.cn/tchMaterial/detail?contentType=assets_document&contentId=2e3dc199-9c42-486b-bbee-7731bd0ee227&catalogType=tchMaterial&subCatalog=dzjc) | （根据2022年版课程标准修订）义务教育教科书·语文六年级上册 | 138 | 20472762 | `e148a13518a9f081d1faa296c88f349ebceb81d426aa3d357958e93cbe752bd4` | 无 |
| [六年级下册](../教材/官方PDF/六年级下册.pdf) | [平台条目](https://basic.smartedu.cn/tchMaterial/detail?contentType=assets_document&contentId=06422d77-21f1-45c3-b409-fa2947eee424&catalogType=tchMaterial&subCatalog=dzjc) | 义务教育教科书·语文六年级下册 | 130 | 14097056 | `878f8d7fba64b1f1277be9a5729952ecccbe1cb2c4ba135f9eb668724d20a683` | 有 |

## 阅读器显示的原文件地址

地址用于记录实际来源，不包含登录令牌；直接打开是否可访问取决于平台授权。

- 一年级上册：[9787107383007_义务教育教科书•语文_一年级_上册_人民教育出版社三科办_1787020686278.pdf](https://r2-ndr-private.ykt.cbern.com.cn/edu_product/esp/assets/1c73b348-e8b6-47d6-84b0-6dbacbe28268.pkg/9787107383007_%E4%B9%89%E5%8A%A1%E6%95%99%E8%82%B2%E6%95%99%E7%A7%91%E4%B9%A6%E2%80%A2%E8%AF%AD%E6%96%87_%E4%B8%80%E5%B9%B4%E7%BA%A7_%E4%B8%8A%E5%86%8C_%E4%BA%BA%E6%B0%91%E6%95%99%E8%82%B2%E5%87%BA%E7%89%88%E7%A4%BE%E4%B8%89%E7%A7%91%E5%8A%9E_1787020686278.pdf)
- 一年级下册：[pdf_1772437264020.pdf](https://r3-ndr-private.ykt.cbern.com.cn/edu_product/esp/assets/b87e153f-a64c-451a-aa6c-6ed9ac7d6821.pkg/pdf_1772437264020.pdf)
- 二年级上册：[9787107397530_义务教育教科书•语文_二年级_上册_人民教育出版社三科办_1787020687283.pdf](https://r2-ndr-private.ykt.cbern.com.cn/edu_product/esp/assets/2ce8f153-7bff-4c97-b6db-9aac414fea19.pkg/9787107397530_%E4%B9%89%E5%8A%A1%E6%95%99%E8%82%B2%E6%95%99%E7%A7%91%E4%B9%A6%E2%80%A2%E8%AF%AD%E6%96%87_%E4%BA%8C%E5%B9%B4%E7%BA%A7_%E4%B8%8A%E5%86%8C_%E4%BA%BA%E6%B0%91%E6%95%99%E8%82%B2%E5%87%BA%E7%89%88%E7%A4%BE%E4%B8%89%E7%A7%91%E5%8A%9E_1787020687283.pdf)
- 二年级下册：[pdf_1772437264737.pdf](https://r1-ndr-private.ykt.cbern.com.cn/edu_product/esp/assets/0f93b83e-b3c2-4a5d-8acd-ea460ab962d4.pkg/pdf_1772437264737.pdf)
- 三年级上册：[9787107397547_义务教育教科书•语文_三年级_上册_人民教育出版社三科办_1787020688089.pdf](https://r3-ndr-private.ykt.cbern.com.cn/edu_product/esp/assets/837f368e-fd4e-404a-ae3f-342d75bc0227.pkg/9787107397547_%E4%B9%89%E5%8A%A1%E6%95%99%E8%82%B2%E6%95%99%E7%A7%91%E4%B9%A6%E2%80%A2%E8%AF%AD%E6%96%87_%E4%B8%89%E5%B9%B4%E7%BA%A7_%E4%B8%8A%E5%86%8C_%E4%BA%BA%E6%B0%91%E6%95%99%E8%82%B2%E5%87%BA%E7%89%88%E7%A4%BE%E4%B8%89%E7%A7%91%E5%8A%9E_1787020688089.pdf)
- 三年级下册：[pdf_1772437265399.pdf](https://r2-ndr-private.ykt.cbern.com.cn/edu_product/esp/assets/8e107655-5128-451f-84e5-d158725c537b.pkg/pdf_1772437265399.pdf)
- 四年级上册：[1111111111111_义务教育教科书•语文_四年级_上册_人民教育出版社三科办_1787020688879.pdf](https://r1-ndr-private.ykt.cbern.com.cn/edu_product/esp/assets/5cd7e623-5c38-4602-871a-3fba8a551db2.pkg/1111111111111_%E4%B9%89%E5%8A%A1%E6%95%99%E8%82%B2%E6%95%99%E7%A7%91%E4%B9%A6%E2%80%A2%E8%AF%AD%E6%96%87_%E5%9B%9B%E5%B9%B4%E7%BA%A7_%E4%B8%8A%E5%86%8C_%E4%BA%BA%E6%B0%91%E6%95%99%E8%82%B2%E5%87%BA%E7%89%88%E7%A4%BE%E4%B8%89%E7%A7%91%E5%8A%9E_1787020688879.pdf)
- 四年级下册：[pdf_1772437266132.pdf](https://r3-ndr-private.ykt.cbern.com.cn/edu_product/esp/assets/53d6315e-5f90-42c4-904f-2d4e95fe99ed.pkg/pdf_1772437266132.pdf)
- 五年级上册：[1111111111111_义务教育教科书•语文_五年级_上册_人民教育出版社三科办_1787020689684.pdf](https://r2-ndr-private.ykt.cbern.com.cn/edu_product/esp/assets/aabf2e4a-3ceb-4e86-8804-22c10223cc57.pkg/1111111111111_%E4%B9%89%E5%8A%A1%E6%95%99%E8%82%B2%E6%95%99%E7%A7%91%E4%B9%A6%E2%80%A2%E8%AF%AD%E6%96%87_%E4%BA%94%E5%B9%B4%E7%BA%A7_%E4%B8%8A%E5%86%8C_%E4%BA%BA%E6%B0%91%E6%95%99%E8%82%B2%E5%87%BA%E7%89%88%E7%A4%BE%E4%B8%89%E7%A7%91%E5%8A%9E_1787020689684.pdf)
- 五年级下册：[pdf_1772437266956.pdf](https://r1-ndr-private.ykt.cbern.com.cn/edu_product/esp/assets/98172dc9-8fba-4da6-9fae-6a3d1166f038.pkg/pdf_1772437266956.pdf)
- 六年级上册：[1111111111111_义务教育教科书•语文_六年级_上册_人民教育出版社三科办_1787020690838.pdf](https://r3-ndr-private.ykt.cbern.com.cn/edu_product/esp/assets/2e3dc199-9c42-486b-bbee-7731bd0ee227.pkg/1111111111111_%E4%B9%89%E5%8A%A1%E6%95%99%E8%82%B2%E6%95%99%E7%A7%91%E4%B9%A6%E2%80%A2%E8%AF%AD%E6%96%87_%E5%85%AD%E5%B9%B4%E7%BA%A7_%E4%B8%8A%E5%86%8C_%E4%BA%BA%E6%B0%91%E6%95%99%E8%82%B2%E5%87%BA%E7%89%88%E7%A4%BE%E4%B8%89%E7%A7%91%E5%8A%9E_1787020690838.pdf)
- 六年级下册：[pdf_1772437267687.pdf](https://r2-ndr-private.ykt.cbern.com.cn/edu_product/esp/assets/06422d77-21f1-45c3-b409-fa2947eee424.pkg/pdf_1772437267687.pdf)
