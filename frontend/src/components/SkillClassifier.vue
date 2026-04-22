<template>
  <div class="section-card">
    <h2>TensorFlow Skill Classifier</h2>

    <el-input
      v-model="inputText"
      type="textarea"
      :rows="4"
      placeholder="Enter one resume sentence, such as: Built backend APIs with FastAPI and Python."
      class="mb-16"
    />

    <div class="button-row">
      <el-button type="primary" :loading="loading" @click="handleClassify">
        Classify
      </el-button>
      <el-button @click="fillExample">
        Load Example
      </el-button>
      <el-button @click="clearResult">
        Clear
      </el-button>
    </div>

    <div v-if="result">
      <el-alert
        :title="`Predicted Label: ${result.label}`"
        type="success"
        :closable="false"
        show-icon
        class="mb-16"
      />

      <el-card class="mb-16">
        <div><strong>Confidence:</strong> {{ result.confidence.toFixed(4) }}</div>
      </el-card>

      <h3>Probabilities</h3>
      <el-card
        v-for="(value, key) in result.probabilities"
        :key="key"
        class="mb-16"
      >
        <div><strong>{{ key }}</strong>: {{ value.toFixed(4) }}</div>
      </el-card>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { ElMessage } from 'element-plus'
import { classifySkill } from '../api/job'

const inputText = ref('')
const loading = ref(false)
const result = ref<{
  label: string
  confidence: number
  probabilities: Record<string, number>
} | null>(null)

const handleClassify = async () => {
  if (!inputText.value.trim()) {
    ElMessage.warning('Please enter a sentence first.')
    return
  }

  try {
    loading.value = true
    result.value = await classifySkill({ text: inputText.value })
  } catch (error) {
    ElMessage.error('Failed to classify the input sentence.')
  } finally {
    loading.value = false
  }
}

const fillExample = () => {
  inputText.value = 'Built backend APIs with FastAPI and Python.'
}

const clearResult = () => {
  inputText.value = ''
  result.value = null
}
</script>