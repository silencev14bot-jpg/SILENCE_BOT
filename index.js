import makeWASocket, {
  useMultiFileAuthState,
  DisconnectReason
} from "@whiskeysockets/baileys"

import fs from "fs"
import path from "path"
import readline from "readline"

const BRIDGE_DIR = "../bridge"
const IN_FILE = path.join(BRIDGE_DIR, "wa_in.json")
const OUT_FILE = path.join(BRIDGE_DIR, "wa_out.json")

const rl = readline.createInterface({
  input: process.stdin,
  output: process.stdout
})

async function start() {
  const { state, saveCreds } = await useMultiFileAuthState("./auth_info")

  const sock = makeWASocket({
    auth: state,
    printQRInTerminal: true // 🔳 QR ALWAYS AVAILABLE
  })

  sock.ev.on("creds.update", saveCreds)

  sock.ev.on("connection.update", (update) => {
    const { connection, lastDisconnect } = update

    if (connection === "open") {
      console.log("✅ WhatsApp connected")
    }

    if (connection === "close") {
      const shouldReconnect =
        lastDisconnect?.error?.output?.statusCode !== DisconnectReason.loggedOut
      if (shouldReconnect) start()
    }
  })

  // 🔢 OPTIONAL PAIRING CODE
  if (!state.creds.registered) {
    rl.question("📱 Enter phone number for pairing (or press Enter to skip): ", async (num) => {
      if (num) {
        const code = await sock.requestPairingCode(num)
        console.log("🔐 Pairing code:", code)
      }
      rl.close()
    })
  }

  sock.ev.on("messages.upsert", async ({ messages }) => {
    const msg = messages[0]
    if (!msg.message || msg.key.fromMe) return

    const jid = msg.key.remoteJid
    const text =
      msg.message.conversation ||
      msg.message.extendedTextMessage?.text

    if (!text) return

    fs.writeFileSync(IN_FILE, JSON.stringify({ user: jid, text }))

    const waitForReply = () =>
      new Promise((resolve) => {
        const i = setInterval(() => {
          if (fs.existsSync(OUT_FILE)) {
            const data = JSON.parse(fs.readFileSync(OUT_FILE))
            fs.unlinkSync(OUT_FILE)
            clearInterval(i)
            resolve(data)
          }
        }, 400)
      })

    const reply = await waitForReply()
    await sock.sendMessage(reply.to, { text: reply.text })
  })
}

start()