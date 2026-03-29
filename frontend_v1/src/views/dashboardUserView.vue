<template>
    <Loader />
    <div class="dashboard_user">
        <nav class="navbar" >
            <img src="../assets/images/manga-oasis logo.png" alt="logo" class="logo">
            <router-link :to="`/user/profile/${user_id}`" class="profile_contain">
                <img :src="get_user_pic(user_data.result['profile_pic'])" alt="profile_pic" class="profile_pic2">
            </router-link>
        </nav>
        <div class="carousel_section">
            <Swiper :autoplay="{delay: 1500,disableOnInteraction: false}" :modules="[Autoplay]">
                <SwiperSlide v-for="i in book_data.result" :key="i">
                    <CarouselSlide :book_value="i" :handle_redirect="handle_redirect" :user_id="user_id"/>
                </SwiperSlide>
            </Swiper> 
        </div>
        <div class="dashboard_sections">
            <div class="first_section">
                <section class="books_section">
                    <header class="books_header">
                        <h1 class="heading3">Our Books</h1>
                        <router-link :to="`/user/books/${user_id}`"><button class="link1">View More</button></router-link>
                    </header>
                    
                    <div class="book_container">
                        <section  class="slide_viewer" v-for="i in book_data.result.slice(0,6)" :key="i">
                            <img :src="get_book_cover(i['book_cover'])" alt="book_cover" class="slide_pic">
                            <div class="carousel_text1">
                                <h1 class="heading4">{{ i["book_name"] }}</h1>
                                <div class="genre_list" >
                                    <p class="genre_name" v-for="j in i['book_genres'].split(',')" :key="j">{{ j }}</p>
                                </div>                   
                                <p class="desc1">{{ i['book_description'].substring(0,170) }},... <span><button class="info_btn" @click="()=>handle_redirect(i['book_id'],user_id)">More Info</button></span> </p>                
                            </div>
                        </section>
                    </div>
                </section>

            </div>
            <div class="secondary_section">
                <aside class="sidebar">
                    <h1 class="section_title">Newly Added</h1>
                    <div v-if="chapter_data.result.length>0" class="sidebar_manga">
                        <div class="manga_section" v-for="i in chapter_data.result.slice(chapter_data.result.length-4)" :key="i">
                            <img class="manga_icon" :src="get_book_cover(get_book_id(i['book_id'])[0]['book_cover'])" alt="manga_pic">
                            <div class="manga_desc">
                                <h3 class="manga_name">{{ get_book_id(i["book_id"])[0]["book_name"] }}</h3>
                                <div class="manga_status">
                                    <p class="manga_add">Vol {{ i["volume_no"] }}</p>
                                    <p class="manga_add">Ch {{ i["chapter_no"] }}</p>
                                </div>
                            </div>
                        </div>
                    </div>
                    <div v-else class="error_state">
                        <p class="error_msg1">No New Chapters</p>
                    </div>
                
                </aside>
                <aside class="sidebar">
                    <h1 class="section_title">Your Collection</h1>
                    <div v-if="accepted_data.result.length>0" class="sidebar_manga">
                        
                        <div class="manga_section" v-for="i in accepted_data.result" :key="i">
                            <img class="manga_icon" :src="get_book_cover(i['book_cover'])" alt="manga_pic">
                            <div class="manga_desc">
                                <h3 class="manga_name">{{ i["book_name"] }}</h3>
                                <div class="manga_status">
                                    <button class="book_read_btn" @click="()=>handle_redirect(i['book_id'],user_id)"> Info</button>
                                    <p class="issued_expiry" v-if="i['status_type']!='buy'" :id="`expiry${i['book_id']}`">{{ countdown_timer(i["expiry"],new Date().getTime(),i['book_id']) }}</p>
                                </div>
                            </div>
                        </div>
                    </div>
                    <div v-else class="error_state">
                        <p class="error_msg1">No Books issued</p>
                    </div>
                </aside>
                <aside class="sidebar">
                    <h1 class="section_title">Order Status</h1>
                    <div v-if="requested_data.result.length>0" class="sidebar_manga">
                        <div class="manga_section" v-for="i in requested_data.result" :key="i">
                            <img class="manga_icon" :src="get_book_cover(get_book_id(i['book_id'])[0]['book_cover'])" alt="manga_pic">
                            <div class="manga_desc">
                                <h3 class="manga_name">{{ i["book_name"] }}</h3>
                                <div class="manga_status">
                                    <p class="manga_add">Requested</p>
                                                
                                </div>
                            </div>
                        </div>
                    </div>
                    <div v-else class="error_state">
                        <p class="error_msg1">No books issue</p>
                    </div>
                    
                </aside>
                <aside class="sidebar">
                    <h1 class="section_title">Your Watchlist</h1>
                    <div v-if="watchlist_data.result.length>0" class="sidebar_manga">
                        <div class="manga_section" v-for="i in watchlist_data.result" :key="i">
                            <img class="manga_icon" :src="get_book_cover(get_book_id(i['book_id'])[0]['book_cover'])" alt="manga_pic">
                            <div class="manga_desc">
                                <h3 class="manga_name">{{ get_book_id(i["book_id"])[0]["book_name"] }}</h3>
                                <div class="manga_status">
                                    <button class="book_read_btn"  @click="()=>handle_redirect(i['book_id'],user_id)">Info</button>
                                    <button class="book_read_btn" @click="()=>remove_watchlist(user_id,i['book_id'])">Remove</button>                
                                </div>
                            </div>
                        </div>
                    </div>
                    <div v-else class="error_state">
                        <p class="error_msg1">Watchlist Empty</p>
                    </div>
                </aside>
                
            </div>
            <PageFooter/>
        
        
        </div>
    </div>
    
</template>

<script setup>
    import PageFooter from '../components/pageFooter.vue'
    import CarouselSlide from '../components/carouselSlide.vue'
    import Loader from '../components/loader.vue'
    import {Swiper, SwiperSlide} from 'swiper/vue'
    import {Autoplay} from 'swiper/modules'
    import 'swiper/css'
    import axios from 'axios'
    import { onMounted, ref } from 'vue';
    import { useRoute } from 'vue-router'

    onMounted(()=>{
        window.scrollTo(0,0)
        get_book_data()
        get_chapter_data()
        get_status()
        get_watchlist()
        get_user_data()
    })
    const route=useRoute()
    const user_id=route.params.id
    const book_data=ref({message:"",result:[]})
    const chapter_data=ref({message:'',result:[]})
    const accepted_data=ref({message:"",result:[]})
    const requested_data=ref({message:"",result:[]})
    const watchlist_data=ref({message:"",result:[]})
    const user_data=ref({message:"",result:[]})

    const get_book_data=()=>{
        const path1="http://localhost:5001/book"
        axios.get(path1,{headers:{Authorization:`Bearer ${localStorage.getItem("access_key")}`}})
            .then((info)=>{
                book_data.value.message=info.data.msg
                book_data.value.result=info.data.result
        })
    }
    const get_user_data=()=>{
        const path1="http://localhost:5001/user"
        axios.get(path1,{headers:{Authorization:`Bearer ${localStorage.getItem("access_key")}`}})
            .then((info)=>{
                let tmp=info.data.result
                user_data.value.message=info.data.msg
                user_data.value.result=tmp.filter((data)=>data["user_id"]==user_id)[0]
        })
    }
    const get_chapter_data=()=>{
        const path1="http://localhost:5001/chapter"
        axios.get(path1,{headers:{Authorization:`Bearer ${localStorage.getItem("access_key")}`}})
            .then((info)=>{
                chapter_data.value.message=info.data.msg
                chapter_data.value.result=info.data.result
        })
    }
    const get_book_id=(id)=>{
        return book_data.value.result.filter((data)=>data["book_id"] ==id)
    }
    const get_status=()=>{
        const path1="http://localhost:5001/get_status"
        
        axios.get(path1,{headers:{Authorization:`Bearer ${localStorage.getItem("access_key")}`}})
            .then((info)=>{
                accepted_data.value.message=info.data.msg
                requested_data.value.message=info.data.msg
                let tmp=info.data.result.filter((data)=>data["status_type"]=="accept" || data["status_type"]=="buy")
                let tmp1=info.data.result.filter((data)=>data["status_type"]=="request")
                accepted_data.value.result=tmp.filter((data)=>data["user_id"]==user_id)
                requested_data.value.result=tmp1.filter((data)=>data["user_id"]==user_id)
            })
    }
    const get_watchlist=()=>{
        const path="http://localhost:5001/watchlist"
        axios.get(path,{headers:{Authorization:`Bearer ${localStorage.getItem("access_key")}`}})
             .then((info)=>{
                watchlist_data.value.message=info.data.msg
                watchlist_data.value.result=info.data.result.filter((data)=>data["user_id"]==user_id)
             })
             
    }
    const remove_watchlist=(user_id,book_id)=>{
        const path=`http://localhost:5001/watchlist/${user_id}/${book_id}`
        axios.delete(path,{headers: {Authorization: `Bearer ${localStorage.getItem("access_key")}`}})
        get_watchlist()
    }
    const get_book_cover=(pic)=>{
        return new URL(`../assets/manga_pics/${pic}`, import.meta.url).href
    }
    const get_user_pic=(pic)=>{
        return new URL(`../assets/images/${pic}`, import.meta.url).href
    }
    const countdown_timer=(expiry_date,now_time,book_id)=>{
        let hrs=expiry_date.split(":")[0]
        let min=expiry_date.split(":")[1]
        let sec=expiry_date.split(":")[2]
        const total_milli=hrs*3600000+min*60000+sec*1000
        const new_time=now_time+total_milli
        let return_time=`${hrs}:${min}:${sec}`
        
        let x=setInterval(()=>{
            let updated_now_time=new Date().getTime()
            let diff=new_time-updated_now_time
            let new_hrs=Math.floor(diff/3600000)
            let new_min=Math.floor((diff%3600000)/60000)
            let new_sec=Math.floor((diff%60000)/1000)
            if(diff>0){
                const path=`http://localhost:5001/status/expiry/${user_id}/${book_id}`
                let payload={'expiry':`${new_hrs}:${new_min}:${new_sec}`}
                axios.put(path,payload,{headers: {Authorization:`Bearer ${localStorage.getItem("access_key")}`}})
                return_time= `${new_hrs}:${new_min}:${new_sec}`
                let ele=document.getElementById(`expiry${book_id}`)
                if(ele){
                    ele.innerHTML=return_time
                }
            }
            else{
                const path=`http://localhost:5001/status/auto_revoke/${user_id}/${book_id}`
                axios.delete(path,{headers: {Authorization:`Bearer ${localStorage.getItem("access_key")}`}})
                stop()
                get_status()
            }
        },3600000)
        let ele=document.getElementById(`expiry${book_id}`)
        if(ele){
            ele.innerHTML=return_time
        }
    }
    const stop=()=>{
        clearInterval(x)
    }
    
</script>
<script>
    export default {
        methods:{
            handle_redirect(id,id1){
                this.$router.push({path:`/user/books/${id}/${id1}`})
            }
        }
    }
</script>
