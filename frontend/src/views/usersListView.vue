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
                        <h1 class="heading">Our Users</h1>
                        <div class="search_bar">
                            <vue-feather type="search" class="icon2" ></vue-feather>
                            <input type="text" name="" id="" @input="(event)=>changeSearchResult(event.target.value)" placeholder="Look for Users..." class="search_input">
                        </div>
                    </div>
                </header>
                    
                <div>
                    <div v-if="search_result.result.length>0" class="user_container">
                        <div class="user_card" v-for="i in search_result.result" :key="i">
                            <div class="user_card_header">
                                <div class="user_card_profile">
                                    <img :src="getImg(i.profile_pic)" alt="profile_pic" class="profile_pic">
                                    <div class="user_card_desc">
                                        <p class="user_card_name">{{ i.user_name }}</p>
                                        <p class="user_card_email">{{ i.email }}</p>
                                    </div>
                                </div>
                                <button class="primary_btn0" @click="()=>removeUser(i.user_id)"><vue-feather type="trash" class="icon2"></vue-feather> Remove</button>
                            </div>
                            <div class="user_card_description1">
                                <p class="user_card_subdesc" @click="()=>booksIssuedModalVisibility(i['user_id'])">Books Issued: <em>{{ i['books_issued'].length }}</em></p>
                                <p class="user_card_subdesc" @click="()=>booksPurchasedModalVisibility(i['user_id'])">Books Purchased: <em>{{ i.books_purchased.length }}</em></p>
                                <p class="user_card_subdesc" @click="()=>feedbacksModalVisibility(i['user_id'])">Feedbacks Provided: <em>{{ i.feedbacks.length }}</em></p>
                            </div>
                            <IssueByBooksModal v-if="booksIssuedModal==i['user_id'] && showBooksIssuedModal" :close_func="booksIssuedModalVisibility" :user_books_issued="i['books_issued']" :getBookById="getIdBook" :getBookCover="getBookCover" />
                            <BooksPurchasedModal v-if="booksPurchasedModal==i['user_id'] && showBooksPurchasedModal" :close_func="booksPurchasedModalVisibility" :user_books_purchased="i.books_purchased" :getBookById="getIdBook" :getBookCover="getBookCover"/>
                            <FeedbacksModal v-if="feedbacksModal==i['user_id'] && showFeedbacksModal" :close_func="feedbacksModalVisibility" :user_feedbacks="i.feedbacks"  :getBookById="getIdBook" :getBookCover="getBookCover"/>
                        </div>
                    </div>
                    <div v-else class="error_state">
                        <p class="error_msg1">No Users Found</p>
                    </div>
                </div>
            </section>
        </div>
        <PageFooter/>
    </div>
                       
</template>



<script setup>
 
    
    import axios from 'axios';
    import { onMounted ,ref} from 'vue';
    import Loader from '@/components/loader.vue';
    import IssueByBooksModal from '../components/issueByBooksModal.vue'
    import BooksPurchasedModal from '../components/booksPurchasedModal.vue'
    import FeedbacksModal from '../components/feedbacksModal.vue'
    import PageFooter from '../components/pageFooter.vue';
   
    onMounted(()=>{
        window.scrollTo(0,0)
        getData()
        getBookData()
    })

    const book_data=ref({message:"",result:[]})
    const user_data=ref({message:"",result:[]})
    const search_result=ref({'result':[]})
    const getBookData=()=>{
        const path="http://localhost:5001/book"
        axios.get(path,{headers:{Authorization:`Bearer ${localStorage.getItem("access_key")}`}})
             .then((data)=>{
                book_data.value.message=data.data.msg
                book_data.value.result=data.data.result
            })
        
    }
    
    const getData = async()=>{
        const path=`http://localhost:5001/user`
        await axios.get(path,{headers:{Authorization:`Bearer ${localStorage.getItem("access_key")}`}})
             .then((data)=>{
                user_data.value.message=data.data.msg
                user_data.value.result=data.data.result
                search_result.value.result=data.data.result
             })
        
    }
    const changeSearchResult=(input)=>{
        search_result.value.result=user_data.value.result.filter((data)=>data['user_name'].toLowerCase().includes(input.toLowerCase()) || data['email'].toLowerCase().includes(input.toLowerCase()))
    }
    const removeUser=async(id)=>{
        const path=`http://localhost:5001/user/${id}`
        await axios.delete(path,{headers:{"Authorization":`Bearer ${localStorage.getItem("access_key")}`}})
        getData()
    }
    const getIdBook=(id)=>{
        return book_data.value.result.filter((info)=>info["book_id"] == id)
    }
    const getBookCover=(id)=>{
        const pic=getIdBook(id)[0]["book_cover"]
        return new URL(`../assets/manga_pics/${pic}`, import.meta.url).href
    }
    const getImg=(pic)=>{
        return new URL(`../assets/images/${pic}`, import.meta.url).href
    }
    
    

</script>

<script>
     export default {
        data(){
            return {
                booksIssuedModal:0,
                booksPurchasedModal:0,
                feedbacksModal:0,
                showFeedbackModal:false,
                showBooksIssuedModal:false,
                showBooksPurchasedModal:false,
            }
        },
        methods:{
            booksIssuedModalVisibility(id){
                this.showBooksIssuedModal=!this.showBooksIssuedModal
                this.booksIssuedModal=id
            },
            booksPurchasedModalVisibility(id){
                this.showBooksPurchasedModal=!this.showBooksPurchasedModal
                this.booksPurchasedModal=id
            },
            feedbacksModalVisibility(id){
                this.showFeedbacksModal=!this.showFeedbacksModal
                this.feedbacksModal=id
            }
        }
     }
</script>