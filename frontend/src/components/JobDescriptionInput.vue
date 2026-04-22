<template>
  <div class="section-card">
    <div class="section-header">
      <h2>Job Description</h2>
      <el-button size="small" @click="loadSample">Load Sample JD</el-button>
    </div>

    <el-input
      v-model="localValue"
      type="textarea"
      :rows="10"
      placeholder="Paste the job description here"
      @input="emitValue"
    />
  </div>
</template>

<script setup lang="ts">
import { ref, watch } from 'vue'

const sampleJD =
  'We are looking for a candidate familiar with Python, FastAPI, REST API, LangChain, RAG, TensorFlow, Git, and basic frontend collaboration.'

const props = defineProps<{
  modelValue: string
}>()

const emit = defineEmits<{
  (e: 'update:modelValue', value: string): void
}>()

const localValue = ref(props.modelValue)

watch(
  () => props.modelValue,
  (newValue) => {
    localValue.value = newValue
  }
)

const emitValue = () => {
  emit('update:modelValue', localValue.value)
}

const loadSample = () => {
  localValue.value = sampleJD
  emitValue()
}
</script>