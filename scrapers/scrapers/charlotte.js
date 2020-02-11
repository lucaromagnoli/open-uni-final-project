const puppeteer = require('puppeteer');
const fs = require('fs');

const autoScroll = async (page) => {
  await page.evaluate(async () => {
    await new Promise((resolve, reject) => {
      let totalHeight = 0;
      let distance = 100;
      let timer = setInterval(() => {
        let scrollHeight = document.body.scrollHeight;
        window.scrollBy(0, distance);
        totalHeight += distance;
        if(totalHeight >= scrollHeight){
          clearInterval(timer);
          resolve()
        }
      }, 100)
    })
  })
};

async function clickMore(page) {
  while(true) {
    await autoScroll(page);
    try {
      let elem = await page.$('button[data-hook="load-more-button"]');
      await elem.click();
    } catch (e) {
      return
    }
  }
}

async function scrape(url) {
  const browser = await puppeteer.launch({headless: true});
  const page = await browser.newPage();
  await page.goto(url);
  await clickMore(page);
  let items = await page.$$eval('li[data-hook="product-list-grid-item"]', lis => {
    let elems = [];
    for (let i= 0; i < lis.length; i++) {
      elems.push(lis[i].querySelector('a').getAttribute('href'));
    }
    return elems
  });
  await browser.close();
  return items
}

(async()=> {
  let seed_urls = [
      'https://www.pelletteriacharlotte.it/donna-borse-a-mano',
      'https://www.pelletteriacharlotte.it/borse-minibag',
      'https://www.pelletteriacharlotte.it/zaini-borse-da-donna',
      'https://www.pelletteriacharlotte.it/borse-a-spalla-donna',
      'https://www.pelletteriacharlotte.it/borse-a-tracolla-donna',
      'https://www.pelletteriacharlotte.it/borse-marsupi-donna'
  ];
  let all_urls = [];
  for (let i = 0; i < seed_urls.length; i++) {
    console.log(`scraping ${seed_urls[i]}`);
    let scraped = await scrape(seed_urls[i]);
    all_urls.push(...scraped);
  }
  fs.writeFileSync('pelletteria-charlotte.txt', all_urls.join('\n'));
})();