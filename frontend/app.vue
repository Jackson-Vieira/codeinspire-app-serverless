<script setup lang="ts">
import { capitalize } from 'vue';

// TODO: PUT in enviroment variable
const url = "https://dzcikln886.execute-api.sa-east-1.amazonaws.com/dev/tips"

// TODO: Move types to a types file
interface Tip {
  code: string
  description: string
  key: string
}

interface TipData {
  tip_language: string
  tip_date: string 
  tip: Tip
}

const { data: tips, pending, error } = await useAsyncData<Array<TipData>>(
  'tips',
  () => $fetch(url)
)

const languages = computed(() => tips.value?.map(tip => tip.tip_language))

const activeTab = ref(0)

function setActiveTab(index: number){
  activeTab.value = index
}

// const tips: Array<TipData> = [
//   {
//     language: "python",
//     tip_date: new Date().toTimeString(),
//     tip: {
//       description: "",
//       code: "",
//       key: ""
//     }
//   },
//   {
//     language: "javascript",
//     tip_date: new Date().toTimeString(),
//     tip: {
//       description: "",
//       code: "",
//       key: ""
//     }
//   },
//   {
//     language: "c++",
//     tip_date: new Date().toTimeString(),
//     tip: {
//       description: "",
//       code: "",
//       key: ""
//     }
//   },
//   {
//     language: "SQL",
//     tip_date: new Date().toTimeString(),
//     tip: {
//       description: "",
//       code: "",
//       key: ""
//     }
//   }
// ]


/* 
-- IDEA --
- Tabs
- Last update date (06/02/2024) (info badge in navbar)
- Github code and documentation
- 5 Languages (Python, Javascript, Go, Rust, C++)

Styles
- Choice a good font to website (OpenSource)
- Dark mode and code highligth (toggler)
- Copyrigth Made with 💚
*/


</script>
<template>
  <main>
    <!-- <div v-if="pending">
      Loading tips...
    </div>

    <div v-else-if="error">
      A error ocurred when loading tips
    </div> -->
    <div class="max-w-screen-md mx-auto space-y-2">
      <h1 class="text-3xl text-center">
        Weekly Tips
      </h1>
      <ul class="flex justify-center gap-4">
        <li 
          v-for="lang, i in languages" 
          class="outline-none hover:border-gray-700 border-transparent border-2 hover:border-current p-1 rounded-sm"
          :class="activeTab === i && 'bg-gray-300'"
        >
         <button
            @click="setActiveTab(i)" 
          >
            {{ capitalize(lang) }}   
          </button>
        </li>
      </ul>

      <div 
          v-for="(tip_data, i) in tips" :key="tip_data.tip_language"
          class="p-2"
          v-show="i == activeTab"
        >
          <div>
            {{ tip_data.tip.description }}
          </div>
          <pre class="border border-gray-300 bg-gray-100 p-1 mt-2 rounded-sm"><code>{{ tip_data.tip.code }}</code></pre>
      </div>
    </div>
  </main>
  <footer class="text-center">
      Made with 💚 <br>
      <a class="underline" href="">Github</a>
  </footer>
</template>

<style scoped>
pre {
  white-space: pre-wrap;
  overflow-x: auto;
}
</style>