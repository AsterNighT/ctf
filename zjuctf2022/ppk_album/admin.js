const puppeteer = require('puppeteer')

const URL = 'http://localhost:5000'
const USERNAME = 'admin'
const PASSWORD = '123456'

async function login(browser) {
    const page = await browser.newPage()
    await page.goto(URL + '/login')
    await page.type('#username', USERNAME)
    await page.type('#password', PASSWORD)
    await page.click('#login-btn')
    await page.close()
}

async function visit(url) {
    const browser = await puppeteer.launch({
        headless: process.env.NODEBUG ?? false,
        args: ['--no-sandbox', '--disable-setuid-sandbox']
    })
    const page = await browser.newPage()
    await login(browser)
    await page.goto(url)
    await new Promise(r => setTimeout(r, 3000))
    await page.close()
    await browser.close()
}

exports.adminVisit = visit