<template>
  <div class="section-card">
    <h2>Career Knowledge Chat</h2>

    <el-input
      v-model="question"
      type="textarea"
      :rows="4"
      placeholder="Ask a question about skills, tools, or learning paths"
      class="mb-16"
    />

    <div class="mb-16">
      <el-tag :type="ragReady ? 'success' : 'warning'">
        {{ ragStatusText }}
      </el-tag>
    </div>

    <div class="button-row">
      <el-button type="primary" :loading="loading" :disabled="!ragReady" @click="handleAsk">
        Ask
      </el-button>
      <el-button @click="fillExample">
        Load Example
      </el-button>
      <el-button @click="clearChat">
        Clear
      </el-button>
    </div>

    <div v-if="answer" class="chat-result">
      <h3>Answer</h3>
      <el-card class="mb-16 answer-card">
        <div class="answer-text">{{ answer }}</div>
      </el-card>

      <div v-if="sources.length" class="mb-16">
        <h3>Sources</h3>
        <div class="tag-list">
          <el-tag
            v-for="sourceItem in sources"
            :key="sourceItem"
            effect="plain"
          >
            {{ sourceItem }}
          </el-tag>
        </div>
      </div>

      <div v-if="retrievedChunks.length">
        <h3>Retrieved Chunks</h3>
        <el-collapse>
          <el-collapse-item
            v-for="(chunk, index) in retrievedChunks"
            :key="index"
            :title="`${chunk.source}`"
            :name="index"
          >
            <pre class="pre-wrap">{{ chunk.content }}</pre>
          </el-collapse-item>
        </el-collapse>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onBeforeUnmount } from 'vue'
import { askRag, getRagStatus } from '../api/job'
import { ElMessage } from 'element-plus'

const question = ref('')
const answer = ref('')
const sources = ref<string[]>([])
const retrievedChunks = ref<{ source: string; content: string }[]>([])
const loading = ref(false)

const ragReady = ref(false)
const ragStatusText = ref('Initializing RAG...')
let pollTimer: number | null = null

const checkRagStatus = async () => {
  try {
    const result = await getRagStatus()

    if (result.status === 'ready') {
      ragReady.value = true
      ragStatusText.value = 'Wikipedia-powered knowledge chat is ready.'
      if (pollTimer) {
        clearInterval(pollTimer)
        pollTimer = null
      }
    } else if (result.status === 'loading') {
      ragReady.value = false
      ragStatusText.value = 'RAG is initializing...'
    } else if (result.status === 'error') {
      ragReady.value = false
      ragStatusText.value = `RAG failed to initialize: ${result.error}`
    } else {
      ragReady.value = false
      ragStatusText.value = 'RAG is not started yet.'
    }
  } catch {
    ragReady.value = false
    ragStatusText.value = 'Unable to check RAG status.'
  }
}

const handleAsk = async () => {
  if (!question.value.trim()) {
    ElMessage.warning('Please enter a question first.')
    return
  }

  if (!ragReady.value) {
    ElMessage.info('RAG is still initializing. Please wait a moment.')
    return
  }

  try {
    loading.value = true
    const result = await askRag({ question: question.value })
    answer.value = result.answer
    sources.value = result.sources || []
    retrievedChunks.value = result.retrieved_chunks || []
  } catch (error) {
    ElMessage.error('Failed to get an answer from the backend.')
  } finally {
    loading.value = false
  }
}

const fillExample = () => {
  question.value = 'What is RAG?'
}

const clearChat = () => {
  question.value = ''
  answer.value = ''
  sources.value = []
  retrievedChunks.value = []
}

onMounted(async () => {
  await checkRagStatus()
  if (!ragReady.value) {
    pollTimer = window.setInterval(checkRagStatus, 2000)
  }
})

onBeforeUnmount(() => {
  if (pollTimer) {
    clearInterval(pollTimer)
    pollTimer = null
  }
})
</script>