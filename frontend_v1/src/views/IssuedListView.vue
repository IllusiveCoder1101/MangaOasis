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
                        <h1 class="heading">Issued Books</h1>
                        
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
                                <div class="issue_card"  >
                                    <div class="issue_profile">
                                        <img :src="getImg(i.profile_pic)" alt="profile_pic" class="profile_pic1">
                                        <div class="user_card_desc">
                                            <p class="user_card_name1">{{i["user_name"]}}</p>
                                            <p class="user_card_email1">{{ i["email"] }}</p>
                                            <p class="issued_expiry" :id="`expiry${i['user_id']}_${i['book_id']}`">{{ i["expiry"] }}</p>
                                        </div>
                                    </div>
                                    <div class="decision_btns">
                                        <button class="btn_secondary0" @click="()=>revoke(i['user_id'],i['book_id'])">Revoke</button>
                                    </div>
                                </div>
            
            
                            </div>
        
                        </div>
                        
                    </div>
                    <div v-else class="error_state">
                        <p class="error_msg1">No Issued Books Found</p>
                    </div>
                    
                </div>
                <div class="new_container">
                     <button @click.prevent="()=>export_csv()" class="primary_btn02" v-if="issued_books_data.result.length>0">Export CSV</button>
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
        get_issued()
    })

    const issued_books_data=ref({"message":"","result":[]})
    const search_result=ref({'result':[]})
    const get_issued=()=>{
        const path=`http://localhost:5001/get_status`
        axios.get(path,{headers:{Authorization:`Bearer ${localStorage.getItem("access_key")}`}})
            .then((info)=>{
                issued_books_data.value.message=info.data.msg
                issued_books_data.value.result=info.data.result.filter((data)=>data.status_type === "accept")
                search_result.value.result=info.data.result.filter((data)=>data.status_type === "accept")
            })
    }
    const changeSearchResult=(input)=>{
        search_result.value.result=issued_books_data.value.result.filter((data)=>data['book_name'].toLowerCase().includes(input.toLowerCase()) || data['book_author'].toLowerCase().includes(input.toLowerCase()) )
    }
    const revoke=(user_id,book_id)=>{
        const path=`http://localhost:5001/status/revoke/${user_id}/${book_id}`
        axios.delete(path,{headers:{"Authorization":`Bearer ${localStorage.getItem("access_key")}`}})
        get_issued()
    }
    const get_book_cover=(pic)=>{
        return new URL(`../assets/manga_pics/${pic}`, import.meta.url).href
    }
    const getImg=(pic)=>{
        return new URL(`../assets/images/${pic}`, import.meta.url).href
    }
    const export_csv=()=>{
       
        let csv_data="Book Name,Book Author,User Name,Email,Expiry\n"
        issued_books_data.value.result.forEach((entry)=>{
            csv_data+=`${entry['book_name']},${entry['book_author']},${entry['user_name']},${entry['email']},${entry['expiry']}\n`
        })
        document.write(csv_data);  
  
     
        const download_trigger = document.createElement('a');  
        download_trigger.href = 'data:text/csv;charset=utf-8,' + encodeURI(csv_data);  
        download_trigger.target = '_blank';  
        
        //provide the name for the CSV file to be downloaded  
        download_trigger.download = 'exported_data.csv';  
        download_trigger.click();  
    }
</script>