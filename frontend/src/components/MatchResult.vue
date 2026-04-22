<template>
  <div class="section-card">
    <h2>Match Analysis</h2>

    <div v-if="result">
      <div class="score-grid mb-16">
        <el-card class="score-card">
          <div class="score-title">Direct Match Score</div>
          <el-progress :percentage="result.direct_match_score" :stroke-width="16" />
        </el-card>

        <el-card class="score-card">
          <div class="score-title">Transferable Background Score</div>
          <el-progress :percentage="result.transferable_background_score" :stroke-width="16" status="success" />
        </el-card>
      </div>

      <div class="result-block">
        <h3>Resume Experience Distribution</h3>
        <div class="tag-list">
          <el-tag type="success" effect="plain">backend: {{ result.resume_experience_distribution.backend || 0 }}</el-tag>
          <el-tag type="warning" effect="plain">frontend: {{ result.resume_experience_distribution.frontend || 0 }}</el-tag>
          <el-tag type="danger" effect="plain">ai_ml: {{ result.resume_experience_distribution.ai_ml || 0 }}</el-tag>
          <el-tag type="info" effect="plain">tools: {{ result.resume_experience_distribution.tools || 0 }}</el-tag>
        </div>
      </div>

      <div class="result-block">
        <h3>Matched Core Skills</h3>
        <div v-if="result.matched_core_skills.length" class="tag-list">
          <el-tag v-for="skill in result.matched_core_skills" :key="skill" type="success" effect="plain">{{ skill }}</el-tag>
        </div>
        <div v-else class="empty-text">No matched core skills found.</div>
      </div>

      <div class="result-block">
        <h3>Missing Technical Skills</h3>
        <div v-if="result.missing_technical_skills.length" class="tag-list">
          <el-tag v-for="skill in result.missing_technical_skills" :key="skill" type="danger" effect="plain">{{ skill }}</el-tag>
        </div>
        <div v-else class="empty-text">No missing technical skills found.</div>
      </div>

      <div class="result-block">
        <h3>Transferable Matches</h3>
        <div v-if="result.transferable_matches.length">
          <el-card v-for="skill in result.transferable_matches" :key="skill" class="suggestion-card">
            <div class="transferable-title">{{ skill }}</div>
            <div class="transferable-evidence">
              Evidence:
              <el-tag
                v-for="evidence in result.transferable_evidence[skill] || []"
                :key="evidence"
                type="warning"
                effect="plain"
                class="transferable-tag"
              >
                {{ evidence }}
              </el-tag>
            </div>
          </el-card>
        </div>
        <div v-else class="empty-text">No transferable matches found.</div>
      </div>

      <div class="result-block">
        <h3>Related Background</h3>
        <div v-if="result.related_background.length" class="tag-list">
          <el-tag v-for="skill in result.related_background" :key="skill" type="warning" effect="plain">{{ skill }}</el-tag>
        </div>
        <div v-else class="empty-text">No related background items found.</div>
      </div>

      <div class="result-block">
        <h3>Learning Suggestions</h3>
        <div v-if="result.learning_suggestions.length">
          <el-card v-for="(item, index) in result.learning_suggestions" :key="index" class="suggestion-card">
            {{ item }}
          </el-card>
        </div>
        <div v-else class="empty-text">No learning suggestions.</div>
      </div>

      <div class="result-block" v-if="hasGroupedMissingSkills">
        <h3>Missing Skills by Category</h3>
        <el-collapse>
          <el-collapse-item
            v-for="(skills, category) in result.grouped_missing_technical_skills"
            :key="category"
            :title="formatCategory(category)"
            :name="category"
          >
            <div class="tag-list">
              <el-tag v-for="skill in skills" :key="skill" type="danger" effect="plain">{{ skill }}</el-tag>
            </div>
          </el-collapse-item>
        </el-collapse>
      </div>

      <div class="result-block">
        <h3>Resume Sentence Classification</h3>
        <el-collapse>
          <el-collapse-item title="View classified resume sentences" name="classified-sentences">
            <div v-if="result.classified_resume_sentences.length">
              <el-card v-for="(item, index) in result.classified_resume_sentences" :key="index" class="suggestion-card">
                <div class="transferable-title">{{ item.label }} ({{ item.confidence.toFixed(4) }})</div>
                <div>{{ item.text }}</div>
              </el-card>
            </div>
            <div v-else class="empty-text">No classified resume sentences.</div>
          </el-collapse-item>
        </el-collapse>
      </div>

      <div class="result-block">
        <h3>Debug Details</h3>
        <el-collapse>
          <el-collapse-item title="Extracted Resume Skills" name="resume-skills">
            <div v-if="result.resume_extracted_skills.length" class="tag-list">
              <el-tag v-for="skill in result.resume_extracted_skills" :key="skill" effect="plain">{{ skill }}</el-tag>
            </div>
            <div v-else class="empty-text">No extracted resume skills.</div>
          </el-collapse-item>

          <el-collapse-item title="Extracted JD Skills" name="jd-skills">
            <div v-if="result.jd_extracted_skills.length" class="tag-list">
              <el-tag v-for="skill in result.jd_extracted_skills" :key="skill" effect="plain">{{ skill }}</el-tag>
            </div>
            <div v-else class="empty-text">No extracted JD skills.</div>
          </el-collapse-item>

          <el-collapse-item title="Hidden Missing Skills" name="hidden-skills">
            <div v-if="result.hidden_missing_skills.length" class="tag-list">
              <el-tag v-for="skill in result.hidden_missing_skills" :key="skill" type="info" effect="plain">{{ skill }}</el-tag>
            </div>
            <div v-else class="empty-text">No hidden missing skills.</div>
          </el-collapse-item>
        </el-collapse>
      </div>
    </div>

    <div v-else class="empty-text">No analysis result yet.</div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'

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

const props = defineProps<{ result: MatchResponse | null }>()

const hasGroupedMissingSkills = computed(() => {
  if (!props.result) return false
  return Object.keys(props.result.grouped_missing_technical_skills || {}).length > 0
})

const formatCategory = (category: string) => {
  return category.replace(/_/g, ' ').replace(/\b\w/g, (char) => char.toUpperCase())
}
</script>
