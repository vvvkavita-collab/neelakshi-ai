import Head from 'next/head'
import Chat from '../components/Chat'

export default function Home(){
  return (
    <>
      <Head>
        <title>Neelakshi AI</title>
        <meta name="description" content="Neelakshi AI — Your bilingual assistant" />
      </Head>
      <div className="min-h-screen bg-gray-50 dark:bg-gray-900 flex items-center justify-center">
        <div className="w-full max-w-3xl p-6">
          <header className="mb-4">
            <h1 className="text-3xl font-bold text-red-600 dark:text-white">Neelakshi AI</h1>
            <p className="text-sm text-gray-600 dark:text-gray-300">Hindi + English assistant — start typing below</p>
          </header>
          <Chat />
        </div>
      </div>
    </>
  )
}
