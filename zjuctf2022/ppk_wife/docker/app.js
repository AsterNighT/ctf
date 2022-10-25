const express = require('express')
const session = require('express-session')
const bodyParser = require('body-parser')
const path = require('path')
const { randomUUID } = require('crypto')

const INVITE_CODE = randomUUID()
const HOST = process.env.NODEBUG ? "0.0.0.0" : "127.0.0.1"
const PORT = process.env.LISTEN_PORT || 5000
const FLAG = process.env.FLAG || 'ZJUCTF{test_flag_h0w_c@n_I_l1ve_w1th0ut_nilou}'

const baseUser = {
    avatar: "nilou1.jpg"
}

const users = []

const app = express()

app.use(bodyParser.text())
app.use(session({
    secret: process.env.SECRET || 'SESE_IS_NOT_PERMITED',
    resave: false,
    saveUninitialized: false,
}))

app.set('view engine', 'hbs');
app.set('views', path.join(__dirname, 'tpls'));

app.use(express.static('./static'))

app.get('/login', (req, res) => {
    res.redirect('/login.html')
})

app.get('/register', (req, res) => {
    res.redirect('/register.html')
})

app.post('/login', (req, res) => {
    let { username, password } = JSON.parse(req.body)
    let r = users.filter(u => u.username == username && u.password == password)
    if (r.length) {
        req.session.user = {
            isAdmin:  r[0].isAdmin,
            username: r[0].username,
            avatar:   r[0].avatar
        }
        res.redirect('/')
    } else {
        res.send('wrong username or password')
    }
})

app.post('/register', (req, res) => {
    let user = JSON.parse(req.body)
    if (!user.username || !user.password) {
        return res.json({ msg: 'empty username or password', err: true })
    }
    if (users.filter(u => u.username == user.username).length) {
        return res.json({ msg: 'username already exists', err: true })
    }
    if (user.isAdmin && user.inviteCode != INVITE_CODE) {
        user.isAdmin = false
        return res.json({ msg: 'invalid invite code', err: true })
    }
    let newUser = Object.assign({}, baseUser, user)
    users.push(newUser)
    res.json({ msg: 'user created successfully', err: false })
})

app.get('/', (req, res) => {
    let user = req.session.user
    if (!user) {
        return res.redirect('/login')
    }
    if (user.isAdmin) {
        res.render('home', {
            user,
            flag: FLAG,
            wife: "you have flag, so no wife"
        })
    } else {
        res.render('home', {
            user,
            flag: "ZJUCTF{no_fl4g_4_u_6ut_you_h@ve_w1fe}",
            wife: "nilou.jpg"
        })
    }
})

app.listen(PORT, HOST, () => {
    console.log(`listening on ${HOST}:${PORT}`)
    console.log(`invite code: ${INVITE_CODE}`)
})