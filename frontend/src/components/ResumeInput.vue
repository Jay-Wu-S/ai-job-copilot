<template>
  <div class="section-card">
    <div class="section-header">
      <h2>Resume Input</h2>
      <el-upload
        :auto-upload="false"
        :show-file-list="false"
        accept=".pdf"
        :on-change="handleFileChange"
      >
        <el-button size="small">Upload Resume (.pdf)</el-button>
      </el-upload>
    </div>

    <div v-if="uploadedFileName" class="uploaded-file">
      Uploaded: {{ uploadedFileName }}
    </div>

    <el-input
      v-model="localValue"
      type="textarea"
      :rows="12"
      placeholder="Upload a PDF resume or paste resume text here"
      @input="emitValue"
    />
  </div>
</template>

<script setup lang="ts">
import { ref, watch } from 'vue'
import { ElMessage } from 'element-plus'
import { uploadResumeFile } from '../api/job'

const props = defineProps<{
  modelValue: string
}>()

const emit = defineEmits<{
  (e: 'update:modelValue', value: string): void
}>()

const localValue = ref(props.modelValue)
const uploadedFileName = ref('')

watch(
  () => props.modelValue,
  (newValue) => {
    localValue.value = newValue
  }
)

const emitValue = () => {
  emit('update:modelValue', localValue.value)
}

const handleFileChange = async (uploadFile: any) => {
  const rawFile = uploadFile.raw as File | undefined

  if (!rawFile) {
    ElMessage.error('Failed to read the selected file.')
    return
  }

  const lowerName = rawFile.name.toLowerCase()

  if (!lowerName.endsWith('.pdf')) {
    ElMessage.warning('Only .pdf files are supported.')
    return
  }

  try {
    const result = await uploadResumeFile(rawFile)
    localValue.value = result.resume_text
    uploadedFileName.value = result.filename
    emitValue()
    ElMessage.success('Resume uploaded successfully.')
  } catch (error: any) {
    const message =
      error?.response?.data?.detail || 'Failed to upload the resume file.'
    ElMessage.error(message)
  }
}
</script>