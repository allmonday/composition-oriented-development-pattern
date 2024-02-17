# fe-demo

## Start
```bash
# run backend
uvicorn src.main:app  --port=8001 --reload


cd fe-demo
npm install
# generate sdk
npm run generate-client
# run
npm run dev
```

开始之后依次查看 `src/pages/SampleXPage.vue`

```js
import {Sample1Service, Sample1TeamDetail} from 'src/client'
import { onMounted, ref } from 'vue';

const teams = ref<Sample1TeamDetail[]>([])

onMounted(async() => {
    teams.value = await Sample1Service.getTeamsWithDetail()
})
```

可以看到使用生成的client sdk, 调用后端接口变得易如反掌.

> 唯一需要注意的是避免后端schema 名称重复 (否则generator会添加额外前缀来保证唯一.)
