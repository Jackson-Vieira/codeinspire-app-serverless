<script setup lang="ts">
import { capitalize } from 'vue';

const TIPS_API_URL = process.env.VUE_APP_TIPS_API_URL || "https://dzcikln886.execute-api.sa-east-1.amazonaws.com/dev/tips";

interface Tip {
  code: string;
  description: string;
  key: string;
}

interface TipData {
  tip_language: string;
  tip_date: string;
  tip: Tip;
}

const { data: tips, pending, error } = await useAsyncData<Array<TipData>>(
  'tips',
  () => $fetch(TIPS_API_URL)
);

const languages = computed(() => tips.value?.map(tip => tip.tip_language));

const activeTab = ref(0);

function setActiveTab(index: number) {
  activeTab.value = index;
}
</script>

<template>
  <div class="bg-zinc-900 flex flex-col text-zinc-300 h-screen">
    <main class="flex-1">
      <div class="max-w-screen-md mx-auto space-y-3 pt-4">
        <h1 class="text-3xl text-center mb-8 underline underline-offset-8">
          Weekly Tips
        </h1>
        
        <div class="text-center" v-if="pending || error">
          <p v-if="error">Ocorreu um erro ao processar sua solicitação. Por favor, tente novamente mais tarde.</p>
          <p v-else>Carregando...</p>
        </div>

        <template v-else>
          <ul class="flex justify-center gap-4">
            <li 
              v-for="(lang, index) in languages" 
              :key="index"
              class="outline-none hover:border-zinc-600 border-transparent border-2 hover:border-current p-1 rounded-md"
              :class="{
                'bg-zinc-700 hover:border-transparent': activeTab === index
              }"
            >
              <button @click="setActiveTab(index)">{{ capitalize(lang) }}</button>
            </li>
          </ul>

          <div 
            v-for="(tipData, index) in tips" 
            :key="tipData.tip_language"
            class="p-2"
            v-show="index === activeTab"
          >
            <div>{{ tipData.tip.description }}</div>
            <pre class="border border-gray-500 bg-zinc-700 p-2 mt-2 rounded-md"><code>{{ tipData.tip.code }}</code></pre>
          </div>
        </template>
      </div>
    </main>
    <footer class="text-center">
      © 2024 - Made with 💚 <br>
      <a class="underline" href="">Github</a>
    </footer>
  </div>
</template>

<style scoped>
pre {
  white-space: pre-wrap;
  overflow-x: auto;
}
</style>