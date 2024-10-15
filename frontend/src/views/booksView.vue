<template>
    <Loader/>
    <div class="books_page">
        <nav class="navbar" >
            <img src="../assets/images/manga-oasis logo.png" alt="logo" class="logo">
        </nav>
        <div class="first_section">
            <section class="books_section">
                <header class="books_header">
                    <div class="search_header">
                        <h1 class="heading">Our Books</h1>
                        <div class="search_bar">
                            <vue-feather type="search" class="icon2" ></vue-feather>
                            <input type="text" name="" id="book_search" @input="(event)=>changeSearchResult(event.target.value)" placeholder="Look for Books..." class="search_input">
                        </div>
                    </div>
                </header>
                <section class="genres_filter">
                    <button :class="(!genres_selected.result.includes(i))?'genre_unselected':'genre_selected'" v-for="i in genre_list.result" :key="i" @click="()=>changeGenreSearch(i)">{{ i }}</button>
                </section>      
                <div >
                    <div v-if="search_result.result.length>0" class="book_container">
                        <section  class="slide_viewer" v-for="i in search_result.result" :key="i">
                            <img :src="get_book_cover(i['book_cover'])" alt="book_cover" class="slide_pic">
                            <div class="carousel_text1">
                                <h1 class="heading4">{{ i["book_name"] }}</h1>
                                <div class="genre_list" >
                                    <p class="genre_name" v-for="j in i['book_genres'].split(',')" :key="j">{{ j }}</p>
                                </div>                   
                                <p class="desc1">{{ i['book_description'].substring(0,200) }},... <span><button class="info_btn" @click="()=>handle_redirect(i['book_id'],user_id)">More Info</button></span> </p>                
                            </div>
                        </section>
                    </div>
                    <div v-else class="error_state">
                        <p class="error_msg1">No Books Found</p>
                    </div>
                </div>
            </section>
        </div>
        <PageFooter/>
    </div>
                       
</template>
<script setup>
    import PageFooter from '../components/pageFooter.vue';
    import { onMounted,ref} from 'vue';
    import { useRoute } from 'vue-router';
    import axios from 'axios';
    import Loader from '@/components/loader.vue';
    onMounted(()=>{
        window.scrollTo(0,0)
        get_book_data()
    })
    const route=useRoute()
    const user_id=route.params.id
    const book_data=ref({message:"",result:[]})
    const genre_list=ref({result:[]})
    const search_result=ref({result:[]})
    const genres_selected=ref({result:[]})
    const get_book_data=()=>{
        const path1="http://localhost:5001/book"
        axios.get(path1,{headers:{"Authorization":`Bearer ${localStorage.getItem("access_key")}`}})
            .then((info)=>{
                book_data.value.message=info.data.msg
                book_data.value.result=info.data.result
                search_result.value.result=info.data.result
                for (let i of book_data.value.result){
                    let genres=i['book_genres'].split(",")
                    for (let j of genres){
                        if(!genre_list.value.result.includes(j)){
                            genre_list.value.result.push(j)
                        }
                    }
                }
        })
    }
    const changeSearchResult=(input)=>{
        search_result.value.result=book_data.value.result.filter((data)=>data['book_name'].toLowerCase().includes(input.toLowerCase()))
    }
    const changeGenreSearch=(input)=>{
        if( genres_selected.value.result.includes(input)){
            genres_selected.value.result.splice(genres_selected.value.result.indexOf(input),1)
        }
        else{
            genres_selected.value.result.push(input)
        }
        const ele=document.getElementById('book_search')
        ele.value=''
        search_result.value.result=book_data.value.result.filter((data)=>data['book_genres'].includes(genres_selected.value.result.toString()))
    }
    const get_book_cover=(pic)=>{
            return new URL(`../assets/manga_pics/${pic}`, import.meta.url).href
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