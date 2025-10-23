import { useState, useRef, useEffect } from 'react'
import axios from 'axios'

export default function Chat(){
  const [messages, setMessages] = useState([
    { role: 'system', text: 'Aap ek helpful assistant ho. Hindi aur English dono me jawab de sakte ho. Primary focus: news-writing in Hindi aur general chat.' }
  ])
  const [input, setInput] = useState('')
  const [loading, setLoading] = useState(false)
  const bottomRef = useRef(null)
  const [theme, setTheme] = useState('auto')

  useEffect(() => {
    // detect system preference
    const dark = window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches
    setTheme(dark ? 'dark' : 'light')
  }, [])

  async function sendMessage(){
    if(!input.trim()) return
    const userMsg = { role: 'user', text: input }
    const newMessages = [...messages, userMsg]
    setMessages(newMessages)
    setInput('')
    setLoading(true)
    try{
      const resp = await axios.post((process.env.NEXT_PUBLIC_API_URL || '') + '/chat', { messages: newMessages })
      const assistantText = resp.data.reply
      setMessages(prev => [...prev, { role: 'assistant', text: assistantText }])
      setLoading(false)
      bottomRef.current?.scrollIntoView({ behavior: 'smooth' })
    }catch(err){
      setMessages(prev => [...prev, { role: 'assistant', text: 'Server error — please try again later.' }])
      setLoading(false)
    }
  }

  return (
    <div className="bg-white dark:bg-gray-800 shadow p-4 rounded-md">
      <div className="space-y-3 h-96 overflow-auto p-2" style={{border: '1px solid #eee'}}>
        {messages.filter(m=>m.role!=='system').map((m, idx)=> (
          <div key={idx} className={m.role === 'user' ? 'text-right' : 'text-left'}>
            <div className={`inline-block p-2 rounded ${m.role==='user'? 'bg-blue-100 dark:bg-blue-900':'bg-gray-100 dark:bg-gray-700'}`}>{m.text}</div>
          </div>
        ))}
        <div ref={bottomRef} />
      </div>

      <div className="mt-3 flex gap-2">
        <input value={input} onChange={(e)=>setInput(e.target.value)} className="flex-1 border rounded p-2 bg-transparent text-black dark:text-white" placeholder="Type in Hindi or English..." />
        <button onClick={sendMessage} className="px-4 py-2 bg-gradient-to-r from-blue-500 to-red-500 text-white rounded" disabled={loading}>{loading? '...' : 'Send'}</button>
      </div>

      <p className="mt-2 text-xs text-gray-500 dark:text-gray-400">Tip: app uses a hosted LLM via your backend. Keep your API key secret.</p>
    </div>
  )
}
