const express = require('express')
const session = require('express-session')
const fileUpload = require('express-fileupload')
const ejs = require('ejs')
const path = require('node:path')
const fs = require('node:fs')
const { randomUUID } = require('node:crypto')
const { adminVisit } = require('./admin')

const HOST = process.env.NODEBUG ? '0.0.0.0' : '127.0.0.1'
const PORT = 5000

const UPLOAD_PATH = path.join(__dirname, 'upload')
const SHARE_DIR = path.join(__dirname, 'share')

const app = express()

app.set('view engine', 'ejs');
app.set('views', path.join(__dirname, 'tpls'));

app.use(express.urlencoded({ extended: true }))

app.use(session({
    secret: process.env.SECRET || 'ZJUCTF{SESE_IS_NOT_PERMITED}',
    resave: false,
    saveUninitialized: false
}))

app.use(fileUpload({
    limits: { fileSize: 5 * 1024 * 1024 }
}))

app.use(express.static('static'))

app.get('/', (req, res) => {
    res.redirect('/home')
})

app.get('/login', (req, res) => {
    res.redirect('/login.html')
})

app.get('/view', (req, res) => {
    let img = req.query.img
    if (!img) {
        res.send('no img specified')
        return
    }
    if (!req.session.username) {
        res.render('302', { target: '/login', delay: 2000, msg: 'login required' })
        return
    }
    res.sendFile(path.join(UPLOAD_PATH, req.session.username, img))
})

app.get('/list', (req, res) => {
    if (!req.session.username) {
        res.render('302', { target: '/login', delay: 2000, msg: 'login required' })
        return
    }
    let userDir = path.join(UPLOAD_PATH, req.session.username)
    if (!fs.existsSync(userDir)) {
        res.send([])
        return
    }
    let imgs = fs.readdirSync(userDir).filter(e => e != '.DS_Store')
    res.send(imgs)
})

app.get('/home', (req, res) => {
    let username = req.session.username
    if (!username) {
        res.render('302', { target: '/login', delay: 2000, msg: 'login required' })
        return
    }
    res.render('home', { username: username })
})

app.post('/login', (req, res) => {
    let username = req.body.username
    if (!username) {
        res.render('302', { target: '/login', delay: 2000, msg: 'username required' })
        return
    }
    if (username.length > 0x30) {
        res.render('302', { target: '/login', delay: 2000, msg: 'the username is too long' })
        return
    }
    if (username == 'admin' && req.socket.remoteAddress != '127.0.0.1') {
        console.log(req.socket.remoteAddress)
        res.render('302', { target: '/login', delay: 2000, msg: 'not allowed' })
        return
    }
    req.session.username = username
    res.redirect('/home')
})

app.post('/upload', (req, res) => {
    let username = req.session.username
    if (!username) {
        res.render('302', { target: '/login', delay: 2000, msg: 'login required' })
        return
    }
    let img = req.files.img
    if (!fs.existsSync(UPLOAD_PATH)) {
        fs.mkdirSync(UPLOAD_PATH)
    }
    let userDir = path.join(UPLOAD_PATH, username)
    if (!fs.existsSync(userDir)) {
        console.log('mkdir', userDir)
        fs.mkdirSync(userDir)
    }
    img.mv(path.join(userDir, img.name), (err) => {
        if (err) {
            res.status(500).send(err)
            return
        }
        res.redirect('/home')
    })
})

app.get('/share', (req, res) => {
    res.redirect('/share.html')
})

app.post('/share2admin', (req, res) => {
    let shareID = req.body.id
    if (!shareID) {
        res.send('no share id?')
        return
    }
    let username = req.session.username
    if (!username) {
        res.send('login required')
        return
    }
    let url = new URL(`http://localhost:5000/viewShare/${username}/${shareID}`)
    adminVisit(url.href)
        .then(() => { res.send('admin will visit your share soon') })
        .catch(() => { res.send('something error') })
})

app.get('/viewShare/:sharer/:id', (req, res) => {
    let shareID = req.params.id
    let sharer = req.params.sharer
    if (!shareID.match(/^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/i)) {
        res.send('invalid share id?')
        return
    }
    let sharePath = path.join(SHARE_DIR, shareID + '.html')
    if (!fs.existsSync(sharePath)) {
        res.render('302', {
            target: '/home',
            delay: 2000,
            msg: `no such share: ${shareID} from ${sharer}`
        })
        return
    }
    res.sendFile(sharePath)
})

app.post('/share', (req, res) => {
    let username = req.session.username
    if (!username) {
        res.render('302', { target: '/login', delay: 2000, msg: 'login required' })
        return
    }
    let img = req.body.img
    if (!img) {
        res.send('image required')
        return
    }
    let imgPath = path.join(UPLOAD_PATH, username, img)
    if (!fs.existsSync(imgPath)) {
        res.send('no such image')
        return
    }
    if (!fs.existsSync(SHARE_DIR)) {
        fs.mkdirSync(SHARE_DIR)
        console.log('mkdir', SHARE_DIR)
    }
    let b64img = 'data:image/png;base64,' + fs.readFileSync(imgPath).toString('base64')
    let tpl = fs.readFileSync(path.join(__dirname, 'tpls', 'share.ejs')).toString()
    let html = ejs.render(tpl, { username: username, img: b64img })
    let pageName = randomUUID()
    fs.writeFileSync(path.join(SHARE_DIR, pageName + '.html'), html)
    res.send(`your share id: ${pageName}`)
})


app.listen(PORT, HOST, () => {
    console.log('listening on', HOST, PORT)
})