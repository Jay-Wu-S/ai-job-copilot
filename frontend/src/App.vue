<template>
  <div class="app-container">
    <div class="page-header">
      <h1>AI Job Copilot</h1>
      <p>
        An AI-powered assistant for resume-job matching, skill gap analysis,
        and knowledge-based career Q&A.
      </p>
    </div>

    <div class="grid-layout">
      <ResumeInput v-model="resumeText" />
      <JobDescriptionInput v-model="jdText" />
    </div>

    <div class="action-panel">
      <el-button type="primary" size="large" :loading="loading" @click="handleAnalyze">
        Analyze Match
      </el-button>
      <el-button size="large" @click="fillSampleResume">
        Load Sample Resume
      </el-button>
      <el-button size="large" @click="clearAll">
        Clear
      </el-button>
    </div>

    <MatchResult :result="matchResult" />
    <RagChat />
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { ElMessage } from 'element-plus'
import ResumeInput from './components/ResumeInput.vue'
import JobDescriptionInput from './components/JobDescriptionInput.vue'
import MatchResult from './components/MatchResult.vue'
import RagChat from './components/RagChat.vue'
import { analyzeMatch } from './api/job'

interface ClassifiedResumeSentence {
  text: string
  label: string
  confidence: number
}

interface MatchResponse {
  matched_core_skills: string[]
  missing_technical_skills: string[]
  related_background: string[]
  transferable_matches: string[]
  transferable_evidence: Record<string, string[]>
  learning_suggestions: string[]
  direct_match_score: number
  transferable_background_score: number
  resume_experience_distribution: Record<string, number>
  classified_resume_sentences: ClassifiedResumeSentence[]
  resume_extracted_skills: string[]
  jd_extracted_skills: string[]
  hidden_missing_skills: string[]
  grouped_missing_technical_skills: Record<string, string[]>
}

const resumeText = ref('')
const jdText = ref('')
const matchResult = ref<MatchResponse | null>(null)
const loading = ref(false)

const fillSampleResume = () => {
  resumeText.value =
    'I know Python, FastAPI, Git, and Vue3. I also built small AI applications with LangChain.'
}

const clearAll = () => {
  resumeText.value = ''
  jdText.value = ''
  matchResult.value = null
}

const handleAnalyze = async () => {
  if (!resumeText.value.trim() || !jdText.value.trim()) {
    ElMessage.warning('Please provide both resume text and job description.')
    return
  }

  try {
    loading.value = true
    matchResult.value = await analyzeMatch({
      resume_text: resumeText.value,
      jd_text: jdText.value,
    })
  } catch (error) {
    ElMessage.error('Failed to analyze the match. Please check the backend.')
  } finally {
    loading.value = false
  }
}
</script>
