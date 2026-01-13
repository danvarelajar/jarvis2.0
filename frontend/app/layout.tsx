import type { Metadata } from 'next'
import { Inter } from 'next/font/google'
import './globals.css'
import { CopilotKit } from '@copilotkit/react-core'
import { CopilotSidebar } from '@copilotkit/react-ui'

const inter = Inter({ subsets: ['latin'] })

export const metadata: Metadata = {
  title: 'Vulnerable AI Agent Laboratory',
  description: 'Educational platform demonstrating OWASP Top 10 LLM and MCP vulnerabilities',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  const backendUrl = process.env.NEXT_PUBLIC_BACKEND_URL || 'http://localhost:8000'
  
  return (
    <html lang="en">
      <body className={inter.className}>
        <CopilotKit runtimeUrl={backendUrl}>
          <CopilotSidebar>
            {children}
          </CopilotSidebar>
        </CopilotKit>
      </body>
    </html>
  )
}
