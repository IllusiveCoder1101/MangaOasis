<template>
    <Loader/>
    <div class="books_page">
        <nav class="navbar" >
            <img src="../assets/images/manga-oasis logo.png" alt="logo" class="logo">
            <router-link to="/user/login"><button class="log_out"><vue-feather type="power" class="icon1" ></vue-feather></button></router-link>
        </nav>
        <div class="first_section">
            <section class="books_section">
                <header class="books_header">
                    <div class="search_header">
                        <h1 class="heading">Issue Books</h1>
                        <div class="search_bar">
                            <vue-feather type="search" class="icon2" ></vue-feather>
                            <input type="text" @input="(event)=>changeSearchResult(event.target.value)" placeholder="Look for Books..." class="search_input">
                        </div>
                    </div>
                </header>   
                <div >
                    <div v-if="search_result.result.length>0" class="user_container">
                        <div class="book_issue_card" v-for="i in search_result.result" :key="i">
                            <div class="user_card_header">
                                <div class="user_card_profile">
                                    <img :src="get_book_cover(i['book_cover'])" alt="manga_pic" class="profile_pic">
                                    <div class="user_card_desc">
                                        <p class="user_card_name">{{ i["book_name"] }}</p>
                                        <p class="user_card_email">{{ i["book_author"] }}</p>
                                    </div>
                                </div>
                            </div>
                            <div class="issue_card_description">
                                <div class="issue_card" >
                                   
                                        <div class="issue_profile" >
                                            <img src="../assets/images/profile_pic.jpg" alt="profile_pic" class="profile_pic1">
                                            <div class="user_card_desc">
                                                <p class="user_card_name1">{{ i["user_name"] }}</p>
                                                <p class="user_card_email1">{{ i["email"] }}</p>
                                                <p class="issued_expiry">{{`${i["expiry"].split(":")[0]}h ${i["expiry"].split(":")[1]}m ${i["expiry"].split(":")[2]}s`}}</p>
                                            </div>
                                        </div>
                                        <div class="decision_btns">
                                            <button class="btn_secondary" @click="()=>update_issue_accept(i['user_id'],i['book_id'])"><vue-feather type="check" class="icon5" ></vue-feather></button>
                                            <button class="btn_secondary1" @click="()=>update_issue_reject(i['user_id'],i['book_id'])"><vue-feather type="x" class="icon5" ></vue-feather></button>
                                        </div>
                                  
                                </div>
                                
                            </div>
        
                        </div>
                    </div>
                    <div v-else class="error_state">
                        <p class="error_msg1">No Issues Found</p>
                    </div>
                    
                </div>
                
            </section>
        </div>
        <PageFooter/>
    </div>
                       
</template>



<script setup>
    import PageFooter from '../components/pageFooter.vue';
    import { onMounted, ref } from 'vue';
    import axios from 'axios';
    import Loader from '@/components/loader.vue';
    onMounted(()=>{
        window.scrollTo(0,0)
        get_issue()
    })

    const issue_books_data=ref({"message":"","result":[]})
    const search_result=ref({'result':[]})
    const get_issue=()=>{
        const path=`http://localhost:5001/get_status`
        axios.get(path,{headers:{Authorization:`Bearer ${localStorage.getItem("access_key")}`}})
            .then((info)=>{
                issue_books_data.value.message=info.data.msg
                issue_books_data.value.result=info.data.result.filter((info)=>info['status_type']=='request')
                search_result.value.result=info.data.result.filter((info)=>info['status_type']=='request')
                
            })
    }
    const changeSearchResult=(input)=>{
        search_result.value.result=issue_books_data.value.result.filter((data)=>data['book_name'].toLowerCase().includes(input.toLowerCase()) || data['book_author'].toLowerCase().includes(input.toLowerCase()) )
    }
    const update_issue_accept=(user_id,book_id)=>{
        const path=`http://localhost:5001/status/accept/${user_id}/${book_id}`
        const payload={"user_id":user_id,"book_id":book_id}
        axios.put(path,payload,{headers:{"Authorization":`Bearer ${localStorage.getItem("access_key")}`}})
             .then(get_issue())
       
    }
    const update_issue_reject=(user_id,book_id)=>{
        const path=`http://localhost:5001/status/reject/${user_id}/${book_id}`
        axios.delete(path,{headers:{"Authorization":`Bearer ${localStorage.getItem("access_key")}`}})
        get_issue()
    }
    const get_book_cover=(pic)=>{
        return new URL(`../assets/manga_pics/${pic}`, import.meta.url).href
    }

</script>