import axios from 'axios'

const api = axios.create({
  baseURL: 'http://127.0.0.1:8000/api',
  timeout: 60000,
})

export interface MatchRequest {
  resume_text: string
  jd_text: string
}

export interface ClassifiedResumeSentence {
  text: string
  label: string
  confidence: number
}

export interface MatchResponse {
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

export interface RagRequest {
  question: string
}

export interface RetrievedChunk {
  source: string
  content: string
}

export interface RagResponse {
  answer: string
  sources: string[]
  retrieved_chunks: RetrievedChunk[]
}

export interface RagStatusResponse {
  status: string
  error: string | null
}

export interface UploadResumeResponse {
  filename: string
  resume_text: string
}

export const analyzeMatch = async (payload: MatchRequest) => {
  const response = await api.post<MatchResponse>('/match', payload)
  return response.data
}

export const askRag = async (payload: RagRequest) => {
  const response = await api.post<RagResponse>('/rag/ask', payload)
  return response.data
}

export const getRagStatus = async () => {
  const response = await api.get<RagStatusResponse>('/rag/status')
  return response.data
}

export const uploadResumeFile = async (file: File) => {
  const formData = new FormData()
  formData.append('file', file)

  const response = await api.post<UploadResumeResponse>('/upload-resume', formData, {
    headers: { 'Content-Type': 'multipart/form-data' },
  })

  return response.data
}
