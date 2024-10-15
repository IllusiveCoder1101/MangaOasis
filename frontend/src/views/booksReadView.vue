<template>
    <Loader/>
    <div class="books_read_page">
        
        <header class="header_1" id="book_read_page_header">
            
            <div class="change_chapter">
                <button @click="()=>changeChapterPrev()" id="prev" class="button_prev"><vue-feather type="chevrons-left"></vue-feather>Prev Chapter</button>
                <div class="book_chapter_container">
                    <div class="options_selector" >
                        <div class="options_menu_btn" @click="()=>optionsVisibility()"><p>{{ `Vol ${current_Chapter_Volume.volume_no} Ch ${current_Chapter_Volume.chapter_no} - ${current_Chapter_Volume.title}`  }}</p>  <vue-feather type="chevron-down"></vue-feather></div>
                        <div class="options_menu" v-if="optionsShow">
                            <button class="option" @click="()=>changeChapterVolume(i['volume_no'],i['chapter_no'],i['index'],i['chapter_title'])" v-for="i in chapter_data.result" :key="i">{{ `Vol ${i['volume_no']} Ch ${i['chapter_no']} - ${i['chapter_title']}` }}</button>
                        </div>
                    </div>
                    <div v-if="buy_status.condition">
                        <button class="download_btn" id="download-chapter" @click.prevent="handle_redirect(user_id,book_id)" ><vue-feather type="download" class="icon"></vue-feather></button>
                    </div>
                </div>    
                <button @click="()=>changeChapterNext()" id="next" class="button_next">Next Chapter <vue-feather type="chevrons-right"></vue-feather></button>
            </div>
        </header>
        <main class="manga_section1" >
            <div class="manga_pages_collection" id="main_read_section">
                <img :src="get_page_img(active_page.res['pic'])"  alt="manga_page" class="manga_page">
            </div>
        </main>
        <footer>
            
            <div class="pagination">
                <img :src="get_page_img(i['pic'])" alt="manga_page" :class="(active_page.res['index']>=i['index'])?'active_page':'manga_page1'"  v-for="i in chapter_pages.result" :key="i">
            </div>
        </footer>
    </div>
</template>

<script setup>
    import { onMounted, ref } from 'vue';
    import axios from 'axios';
    import { useRoute } from 'vue-router';
    import Loader from '@/components/loader.vue';
    
    const route=useRoute()
    const book_id=route.params.id
    const user_id=route.params.id1
    const current_Chapter_Volume=ref({'chapter_no':1,'volume_no':1,'index':1,'title':''})
    
    onMounted(()=>{
        window.scrollTo(0,0)
        get_chapter()
        buy_status_check()
    })
    
    const chapter_data=ref({"result":[]})
    const chapter_pages=ref({'result':[]})
    const active_page=ref({'res':{}})
    const buy_status=ref({"condition":false})
    const download_chapter=ref({"res":''})
    document.addEventListener("keydown",(event)=>{
        if(event.key=="ArrowRight" ){
            changePageById(active_page.value.res.index<chapter_pages.value.result.length?active_page.value.res.index+1:1)
        }
        if(event.key=="ArrowLeft" ){
            changePageById(active_page.value.res.index>1?active_page.value.res.index-1:chapter_pages.value.result.length)
        }
    })
    document.addEventListener("click",(event)=>{
        if(event.pageX>window.innerWidth/2 && event.target.id==='main_read_section'){
            changePageById(active_page.value.res.index<chapter_pages.value.result.length?active_page.value.res.index+1:1)

        }
        if(event.pageX<window.innerWidth/2 && event.target.id==='main_read_section'){
            changePageById(active_page.value.res.index>1?active_page.value.res.index-1:chapter_pages.value.result.length)            
        }
    })

    const get_chapter=()=>{
        const path='http://localhost:5001/chapter'
        axios.get(path,{headers: {Authorization:`Bearer ${localStorage.getItem("access_key")}`}})
             .then((info)=>{
                let tmp=info.data.result
                let index=1
                chapter_data.value.result=tmp.filter((data)=>data['book_id']==book_id).map((info)=>{
                    let obj={...info,"index":index}
                    index+=1
                    return obj
                })
                current_Chapter_Volume.value.title=chapter_data.value.result[0]['chapter_title']
                get_chapter_page(current_Chapter_Volume.value.chapter_no,current_Chapter_Volume.value.volume_no)        
             })
        
    }
    
    const buy_status_check=async()=>{
        const path2="http://localhost:5001/get_status"
        await axios.get(path2,{headers:{"Authorization":`Bearer ${localStorage.getItem("access_key")}`}})
            .then((info)=>{
                let tmp=info.data.result.filter((data)=>data["book_id"]==book_id && data['user_id']==user_id && data["status_type"]=="buy")
                buy_status.value.condition=tmp.length>0
            })

    }
    const get_chapter_id=(ch_no,vol_no)=>{
        return chapter_data.value.result.filter((info)=>info['chapter_no']==ch_no && info['volume_no']==vol_no)
    }
    const get_page_img=(img)=>{
        return new URL(`../assets/manga_pics/${img}`, import.meta.url).href
    }
    const get_chapter_page=(ch_no,vol_no)=>{
        const data=get_chapter_id(ch_no,vol_no)[0]['chapter_pages']
        let ctr=1
        chapter_pages.value.result=data.split(",").map((info)=>{
            let obj={"index":ctr,"pic":info}
            ctr+=1
            return obj
        })
        active_page.value.res=chapter_pages.value.result[0]
        let tmp=active_page.value.res.pic.substring(0,active_page.value.res.pic.length-4).split("-")
        console.log(tmp)
        for(let i of tmp){
            if(i!=="page"){
                download_chapter.value.res+=i+"-"
            }
            else{
                break
            }
        }
        console.log(download_chapter.value.res.substring(0,download_chapter.value.res.length-1))
    }
    const changeChapterNext=()=>{
        current_Chapter_Volume.value.index= current_Chapter_Volume.value.index<chapter_data.value.result.length ? current_Chapter_Volume.value.index+=1:1
        changeCurrentChapter()
    }
    const changeChapterPrev=()=>{
        current_Chapter_Volume.value.index=current_Chapter_Volume.value.index>1 ? current_Chapter_Volume.value.index-1:chapter_data.value.result.length
        changeCurrentChapter()
    }
    const changeCurrentChapter=()=>{
        current_Chapter_Volume.value.volume_no=chapter_data.value.result.filter((data)=>data.index===current_Chapter_Volume.value.index)[0]['volume_no']
        current_Chapter_Volume.value.chapter_no=chapter_data.value.result.filter((data)=>data.index===current_Chapter_Volume.value.index)[0]['chapter_no']        
        current_Chapter_Volume.value.title=chapter_data.value.result.filter((data)=>data.index===current_Chapter_Volume.value.index)[0]['chapter_title']
        get_chapter_page(current_Chapter_Volume.value.chapter_no,current_Chapter_Volume.value.volume_no)
    }
    const changePageById=(indx)=>{
        active_page.value.res=chapter_pages.value.result.filter((info)=>info.index==indx)[0]
    }
    const changeChapterVolume=(vol_no,ch_no,indx,title)=>{
        current_Chapter_Volume.value.index=indx
        current_Chapter_Volume.value.volume_no=vol_no
        current_Chapter_Volume.value.chapter_no=ch_no
        current_Chapter_Volume.value.title=title
        get_chapter_page(current_Chapter_Volume.value.chapter_no,current_Chapter_Volume.value.volume_no)
    }
   
</script>

<script>
    export default {
        data(){
            return { 
                optionsShow:false
            }
        },
        methods:{
            optionsVisibility(){
                this.optionsShow =!this.optionsShow
            },
            handle_redirect(id,id1){

        
                this.$router.push({path:`/user/preview/books/${id}/${id1}`})
          
            }
        }
    }
</script>