// components/chat/ChatInterface.tsx (Updated)
'use client'

import React, { useState } from 'react'
import Header from '@/components/layout/Header'
import Sidebar from '@/components/layout/Sidebar'
import MessageList from './MessageList'
import InputArea from './InputArea'
import SettingsPanel from '@/components/settings/SettingsPanel'

export default function ChatInterface() {
  const [showSidebar, setShowSidebar] = useState(false)
  const [showSettings, setShowSettings] = useState(false)

  return (
    <div className="flex h-screen bg-gray-50 dark:bg-gray-950">
      {/* Sidebar */}
      <Sidebar isOpen={showSidebar} onClose={() => setShowSidebar(false)} />

      {/* Main Content */}
      <div className="flex-1 flex flex-col overflow-hidden">
        {/* Header */}
        <Header onMenuClick={() => setShowSidebar(true)} />

        {/* Chat Area */}
        <div className="flex-1 flex flex-col overflow-hidden">
          <MessageList />
          <InputArea onSettingsClick={() => setShowSettings(true)} />
        </div>
      </div>

      {/* Settings Modal */}
      <SettingsPanel open={showSettings} onOpenChange={setShowSettings} />
    </div>
  )
}
