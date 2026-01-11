import puppeteer from "puppeteer";
import XLSX from "xlsx";

const delay = (ms) => new Promise(res => setTimeout(res, ms));
let stopRequested = false;

process.stdin.resume();
process.stdin.setEncoding('utf8');
console.log('Ketik "stop" lalu Enter untuk berhenti dan menyimpan data.');
process.stdin.on('data', (input) => {
    const cmd = input.trim().toLowerCase();
    if (cmd === 'stop' || cmd === 'exit') {
        stopRequested = true;
        console.log('Perintah Stop diterima. Menyelesaikan item saat ini lalu menyimpan...');
    }
});

process.on('SIGINT', () => {
    stopRequested = true;
    console.log('SIGINT received. Stopping gracefully...');
});

async function getGoogleMapsData(keyword, maxItems = 20) {
    let browser;
    try {
        browser = await puppeteer.launch({
            headless: false,
            defaultViewport: null,
            args: ["--start-fullscreen"]
        });

        const page = (await browser.pages())[0];

        const url = `https://www.google.com/maps/search/${encodeURIComponent(keyword)}`;
        await page.goto(url, { waitUntil: ["domcontentloaded", "networkidle2"] });

        await page.waitForSelector('div[role="feed"]');
        const scrollableSelector = 'div[role="feed"]';

        const collectedData = [];
        const uniqueItems = new Set();

        console.log(`🚀 Sedang mengambil data: "${keyword}"...`);

        let lastProcessedIndex = 0;
        let prevFeedHeight = 0;

        while (!stopRequested && collectedData.length < maxItems) {

            const cards = await page.$$('.Nv2PK');

            if (lastProcessedIndex >= cards.length) {

                const currentFeedHeight = await page.evaluate(sel => {
                    const el = document.querySelector(sel);
                    if (!el) return 0;
                    el.scrollBy(0, 500);
                    return el.scrollHeight;
                }, scrollableSelector);

                await delay(3000);

                if (currentFeedHeight === prevFeedHeight) {
                    console.log("🛑 Scroll mentok. Tidak ada card baru.");
                    break;
                }

                prevFeedHeight = currentFeedHeight;
                continue;
            }

            const card = cards[lastProcessedIndex];
            lastProcessedIndex++;

            try {
                await card.evaluate(el => el.scrollIntoView({ block: 'center' }));
                await delay(500);
                try {
                    await card.click({ clickCount: 2 });
                } catch (err) {
                    await page.evaluate(el => el.click(), card);
                }

                try {
                    await page.waitForSelector('[role="article"]')
                } catch (_) { }
                await delay(3000);

                if (stopRequested) break;

                const nama = await card.$eval('.qBF1Pd', el => el.textContent.trim())
                if (!nama || uniqueItems.has(nama)) {
                    await closeDetail(page);
                    continue;
                }

                const rating = await card.$eval('.MW4etd', el => el.textContent.trim()).catch(() => "N/A");
                const link = await card.$eval('a.hfpxzc', el => el.href).catch(() => "N/A");
                let alamat = ''
                try {
                    alamat = await card.$eval('.W4Efsd > span:nth-child(2)', els => els.textContent.replace('·', '').trim());
                } catch (error) {
                    alamat = await card.$$eval('.W4Efsd', els =>
                        els.length > 1 ? els[1].textContent.replace("·", "").trim() : "N/A"
                    );
                }

                await openReviewTab(page);

                const linkImage = await card.$eval(
                    '[role="article"] img[decoding="async"]',
                    el => el.src
                ).catch(() => null);

                const totalUlasan = await page.evaluate(() => {
                    const el = document.querySelector('.fontDisplayLarge');
                    if (!el) return "N/A";
                    const sib = el.parentElement?.querySelector('div.fontBodySmall');
                    return sib ? sib.textContent.replace(/\D/g, '') : "N/A";
                });

                if (totalUlasan === "N/A") {
                    await closeDetail(page);
                    continue;
                }

                const keywords = await page.evaluate(() => {
                    const nodes = document
                        .querySelectorAll('button.e2moi > div > span.fontBodyMedium');
                    return [...nodes].slice(1, -1).map(x => x.innerText.toLowerCase());
                });

                const reviews = await extractReviews(page);
                if (!reviews.length) {
                    await closeDetail(page);
                    continue;
                }

                uniqueItems.add(nama);
                collectedData.push({
                    "Link Gambar": linkImage,
                    "Nama Kafe": nama,
                    "Alamat": alamat,
                    "Rating": rating,
                    "Link Maps": link,
                    "Keywords": keywords.join(', '),
                    "Total Ulasan": totalUlasan,
                    "Ulasan": JSON.stringify(reviews)
                });

                console.log(`✔ ${collectedData.length}. ${nama}`);

                await closeDetail(page);
                await delay(2000);

            } catch (err) {
                console.log("⚠️ Error:", err.message);
            }
        }

        return collectedData;

    } catch (error) {
        console.error("Fatal Error:", error);
        return [];
    } finally {
        if (browser) {
            try { await browser.close(); } catch (e) { }
        }
    }
}

async function closeDetail(page) {
    try {
        await page.waitForSelector('button[aria-label="Tutup"]', {
            visible: true
        }).catch(() => { });

        await page.evaluate(() => {
            const buttons = Array.from(
                document.querySelectorAll('button[aria-label="Tutup"]')
            )[1];

            if (buttons) buttons.click();
        });

        await delay(3000);
    } catch {}
}


async function openReviewTab(page) {
    try {
        await page.waitForSelector('button[role="tab"]', { visible: true, timeout: 5000 });
        const tabs = await page.$$('button[role="tab"]');
        const idx = tabs.length > 3 ? 2 : 1;
        if (tabs[idx]) {
            await tabs[idx].evaluate(el => el.scrollIntoView({ block: 'center' }));
            await delay(300);
            await tabs[idx].click({ clickCount: 2 });
            await delay(2500);
        }
    } catch { }
}

async function extractReviews(page, maxReviews = 30) {
    try {
        await page.waitForSelector('.MyEned > span:nth-child(1)');

        let prevHeight = -1;
        let sameHeightCount = 0;

        while (sameHeightCount < 2) {
            const newHeight = await page.evaluate(() => {
                const anchor = document.querySelector('.fontDisplayLarge');
                if (!anchor) return 0;

                let panel = anchor;
                for (let i = 0; i < 4; i++) panel = panel?.parentElement;
                if (!panel) return 0;

                panel.scrollBy(0, panel.scrollHeight);
                return panel.scrollHeight + panel.scrollTop;
            });

            if (!newHeight || newHeight === prevHeight) {
                sameHeightCount++;
            } else {
                sameHeightCount = 0;
            }

            prevHeight = newHeight;
            await delay(1500);
        }

        const reviews = await page.evaluate((limit) => {
            const results = [];

            const reviewEls = document.querySelectorAll(
                '.MyEned > span:nth-child(1)'
            );

            const ratingEls =
                document.querySelector('.MyEned')
                    ?.parentElement?.parentElement
                    ?.parentElement?.parentElement
                    ?.parentElement?.parentElement
                    ?.querySelectorAll('span[role="img"]') || [];

            for (let i = 0; i < reviewEls.length && results.length < limit; i++) {
                const text = reviewEls[i].innerText.trim();
                if (!text) continue;

                let rating = "N/A";
                try {
                    const r = ratingEls[i];
                    if (r) {
                        rating = r
                            .getAttribute('aria-label')
                            ?.toLowerCase()
                            .replace('bintang', '')
                            .trim();
                    }
                } catch { }

                results.push({
                    Rating: rating,
                    Ulasan: text
                });
            }

            return results;
        }, maxReviews);

        return reviews;

    } catch (err) {
        console.log("⚠️ extractReviews failed:", err.message);
        return [];
    }
}

// ================= EXECUTION =================
(async () => {
    const keyword = "Coffee Shop Malang";

    const data = await getGoogleMapsData(keyword, 50);

    if (!data.length) {
        console.log("❌ Tidak ada data yang tersimpan.");
    } else {
        const worksheet = XLSX.utils.json_to_sheet(data);
        const workbook = XLSX.utils.book_new();
        XLSX.utils.book_append_sheet(workbook, worksheet, "Data Kafe");

        XLSX.writeFile(workbook, "data_mentah/List_Kafe_Malang_Lengkap.xlsx");
        console.log(`✅ SUKSES! ${data.length} data tersimpan di 'data_mentah/List_Kafe_Malang_Lengkap.xlsx'`);
    }

    process.exit(0);
})();