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

开始之后依次查看 `src/pages/SampleXPage.vue`, 以Sample1为例.
backend:
```python
@route.get('/teams-with-detail', response_model=List[Sample1TeamDetail])
async def get_teams_with_detail(session: AsyncSession = Depends(db.get_session)):
    """ 1.6 return list of team(sprint(story(task(user)))) """
    teams = await tmq.get_teams(session)
    teams = [Sample1TeamDetail.model_validate(t) for t in teams]
    teams = await Resolver().resolve(teams)
    return teams
```

frontend:
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
