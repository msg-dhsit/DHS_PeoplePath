const restify = require('restify')
const { ActivityHandler, CloudAdapter, ConfigurationServiceClientCredentialFactory, MemoryStorage, ConversationState, UserState } = require('botbuilder')

const server = restify.createServer()
server.use(restify.plugins.bodyParser())

const credentialsFactory = new ConfigurationServiceClientCredentialFactory({
  MicrosoftAppId: process.env.MICROSOFT_APP_ID || '',
  MicrosoftAppPassword: process.env.MICROSOFT_APP_PASSWORD || '',
  MicrosoftAppType: 'MultiTenant'
})

const adapter = new CloudAdapter(credentialsFactory)
const conversationState = new ConversationState(new MemoryStorage())
const userState = new UserState(new MemoryStorage())

class TeamsBot extends ActivityHandler {
  constructor() {
    super()
    this.onMessage(async (context, next) => {
      const text = context.activity.text || ''
      if (text.startsWith('/timesheet suggest')) {
        await context.sendActivity('AI suggestions ready: open portal to review timesheet.')
      } else if (text.startsWith('/timesheet status')) {
        await context.sendActivity('Current week status: submitted')
      } else {
        await context.sendActivity('Try /timesheet suggest or /timesheet status')
      }
      await next()
    })
  }
}

const bot = new TeamsBot()

server.post('/api/messages', async (req, res) => {
  await adapter.process(req, res, (context) => bot.run(context))
})

const port = process.env.PORT || 3978
server.listen(port, () => {
  console.log(`Bot listening on ${port}`)
})
