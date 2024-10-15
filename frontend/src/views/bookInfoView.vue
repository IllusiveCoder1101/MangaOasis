<template>
    <Loader/>
    <div class="books_page">
        <nav class="navbar" >
            <img src="../assets/images/manga-oasis logo.png" alt="logo" class="logo">
            
        </nav>
        <div v-if="book_data.result.length>0">
            <header class="books_info_header">
            <img :src="get_book_cover(book_data.result[0]['book_cover'])" alt="manga_background_pic" class="carousel_img">
            <div class="manga_desc1">
                <img :src="get_book_cover(book_data.result[0]['book_cover'])" alt="manga_hero_img" class="hero_img">
                <div class="desc">
                    <h1 class="heading">{{ book_data.result[0]['book_name'] }}</h1>
                    <h3 class="sub_heading2"> {{ book_data.result[0]['author_name'] }}</h3>
                    <div class="sub_desc">
                        <div class="genre_list">
                            <p class="genre_name" v-for="i in book_data.result[0]['book_genres'].split(',')" :key="i">{{ i }}</p>
                            
                        </div>
                        <div class="status_list">
                            <p class="status" v-if="book_data.result[0]['chapters'].length>0">Vol {{ book_data.result[0]['chapters'][book_data.result[0]['chapters'].length - 1]['volume_no' ]  }}</p>
                            <p class="status" v-if="book_data.result[0]['chapters'].length>0">Ch {{ book_data.result[0]['chapters'][book_data.result[0]['chapters'].length - 1]['chapter_no' ]  }}</p>
                            <p class="status" v-else>No chapters</p>
                        </div>
                    </div>
                    <div class="btn_container">
                        <button class="primary_btn" @click="()=>handlePaymentModal(buy_status_check.pass,status_check.pass,book_data.result[0]['chapters'].length>0)"><vue-feather type="tag" class="icon2"/> Pay</button>
                        <button class="primary_btn" @click="()=>handleRequestModal(request_status_check.pass,request_status_check.pass1,status_check.pass,buy_status_check.pass,book_data.result[0]['chapters'].length>0)"><vue-feather type="plus" class="icon2"/> Request Access</button>
                        <button class="primary_btn"  @click="()=>add_to_watchlist()"><vue-feather type="bookmark" class="icon2"/>Add to Watchlist</button>
                        <button class="primary_btn"  @click="()=>handle_redirect(book_id,user_id,(!buy_status_check.pass || !status_check.pass))"><vue-feather type="book-open" class="icon2"/> Start Reading</button>
                    </div>
                </div>

            </div>
            </header>
            <PaymentModal v-if="showPaymentModal" :close_func="handlePaymentModal" :book_data="book_data.result" :handle_submit="pay_book"/>
            <ReviewModal v-if="showReviewModal" :close_func="handleReviewModal" :handle_submit="post_feedback"/>
            <RequestModal v-if="showRequestModal" :close_func="handleRequestModal" :handle_submit="request_book"/>
            <section class="manga_description">
                <h1 class="title">About <em>Manga</em></h1>
                <p class="desc">{{ book_data.result[0]['book_description'] }}</p>
            </section>
            <section class="reviews">
                <div class="header_section">
                    <h1 class="title1">Reviews</h1>
                    <button class="secondary_btn" @click="()=>handleReviewModal()"><vue-feather type="plus" class="icon2"/>Reviews</button>
                </div>
                <div class="review_container">
                    <div v-if="feedback_data.result.length>0">
                        <div class="review" v-for="i in feedback_data.result" :key="i">
                            <div class="review_header">
                                <div class="profile_desc">
                                    <img :src="get_user_pic(get_user_id(i['user_id'])[0]['profile_pic']) || ''" alt="profile_pic" class="profile_pic">
                                    <div class="profile_text">
                                        <p class="name">{{ (get_user_id(i['user_id'])[0]['user_name']) }}</p>
                                        <div v-if="i['user_id']==user_id" class="button_container">
                                            <button class="primary_btn_1" @click.prevent="()=>handleEditFeedbackModal(i['feedback_id'])"> <vue-feather type="edit" ></vue-feather></button>
                                            <button class="primary_btn_1" @click.prevent="()=>remove_feedback(i['feedback_id'])"><vue-feather type="trash" ></vue-feather></button>
                                            <EditFeedbackModal v-if="editFeedbackModal==i['feedback_id'] && showEditFeedbackModal" :close_func="handleEditFeedbackModal" :handle_submit="edit_feedback" :data="getIdFeedback(i['feedback_id'])"/>
                                        </div>
                                    </div>
                                </div>
                                <h2 class="score">{{ i['feedback_score'] }} <em>/ 10</em></h2>
                            </div>
                            <div class="review_desc">
                                <p class="desc">{{ i['feedback_message'] }}</p>
                            </div>
                        </div>
                    </div>
                    <div v-else class="error_state">
                        <p class="error_msg1">No Feedbacks</p>
                    </div>
                </div>
            </section>
        </div>
        <pageFooter/>
    </div>
                       
</template>

<script setup>
    
    import pageFooter from '@/components/pageFooter.vue';
    import PaymentModal from '../components/paymentModal.vue'
    import ReviewModal from '../components/reviewModal.vue'
    import RequestModal from '../components/requestModal.vue'
    import { onMounted, ref } from 'vue';
    import { useRoute } from 'vue-router';
    import axios from 'axios';
    import Loader from '@/components/loader.vue';
    import EditFeedbackModal from '../components/editFeedbackModal.vue'
    const route=useRoute()
    const book_id=route.params.id
    const user_id=route.params.id1
    
    onMounted(()=>{
        window.scrollTo(0,0)
        get_book_data()
        get_feedbacks()
        get_user()
        clearInterval()
    })
    
    const book_data=ref({"message":"","result":[]})
    const feedback_data=ref({"message":"","result":[]})
    const user_data=ref({"message":"",result:[]})
    const status_check=ref({pass:false})
    const watchlist_check=ref({pass:false})
    const buy_status_check=ref({pass:false})
    const request_status_check=ref({pass:false,pass1:false})
    const get_book_data=()=>{
        const path1="http://localhost:5001/book"
        axios.get(path1,{headers:{"Authorization":`Bearer ${localStorage.getItem("access_key")}`}})
            .then((info)=>{
                book_data.value.message=info.data.msg
                book_data.value.result=info.data.result.filter((info)=>info['book_id']==book_id)
        })
        check_status()
        check_buy_status()
        check_watchlist()
        check_request_status()
    }
    
    const check_watchlist=()=>{
        const path='http://localhost:5001/watchlist'
        axios.get(path,{headers:{"Authorization":`Bearer ${localStorage.getItem("access_key")}`}})
             .then((info)=>{
                watchlist_check.value.pass=(info.data.result).filter((data)=>data['book_id']==book_id && data['user_id']==user_id).length>0
             })
    }
    const check_request_status=()=>{
        const path='http://localhost:5001/get_status'
        axios.get(path,{headers:{"Authorization":`Bearer ${localStorage.getItem("access_key")}`}})
             .then((info)=>{
                let tmp=info.data.result
                request_status_check.value.pass=tmp.filter((data)=>(data['status_type']=='request' ) && data['user_id']==user_id ).length==5?false:true
                request_status_check.value.pass1=tmp.filter((data)=>(data['status_type']=='request' ) && data['book_id']==book_id && data['user_id']==user_id).length>0?false:true
            })
    }
    const check_status=()=>{
        const path='http://localhost:5001/get_status'
        axios.get(path,{headers:{"Authorization":`Bearer ${localStorage.getItem("access_key")}`}})
             .then((info)=>{
                let tmp=info.data.result
                status_check.value.pass=tmp.filter((data)=>data['book_id']==book_id && data['user_id']==user_id && data['status_type']=='accept').length>0?false:true
             })
    }
    const check_buy_status=()=>{
        const path='http://localhost:5001/get_status'
        axios.get(path,{headers:{"Authorization":`Bearer ${localStorage.getItem("access_key")}`}})
             .then((info)=>{
                let tmp=info.data.result
                buy_status_check.value.pass=tmp.filter((data)=>data['book_id']==book_id && data['user_id']==user_id && (data['status_type']=='buy')).length>0?false:true
             })
        
    }
    
    const get_book_cover=(pic)=>{
            return new URL(`../assets/manga_pics/${pic}`, import.meta.url).href
    }
    
    const get_user_pic=(pic)=>{
            return new URL(`../assets/images/${pic}`, import.meta.url).href
    }
    
    const get_feedbacks=()=>{
        const path="http://localhost:5001/feedback"
        axios.get(path,{headers:{"Authorization":`Bearer ${localStorage.getItem("access_key")}`}})
             .then((info)=>{
                feedback_data.value.message=info.data.msg
                feedback_data.value.result=info.data.result.filter((info)=>info['book_id']==book_id)
             })
    }
    const getIdFeedback=(feedback_id)=>{
        return feedback_data.value.result.filter((info)=>info['feedback_id']==feedback_id)[0]
    }
    const edit_feedback=(feedback_id,payload)=>{
        const path=`http://localhost:5001/feedback/${feedback_id}`
        axios.put(path,payload,{headers:{"Authorization":`Bearer ${localStorage.getItem("access_key")}`}})
        get_feedbacks()
        
    }
    const remove_feedback=(feedback_id)=>{
        const path=`http://localhost:5001/feedback/${feedback_id}`
        axios.delete(path,{headers:{"Authorization":`Bearer ${localStorage.getItem("access_key")}`}})
        get_feedbacks()

    }
    const get_user=()=>{
        const path='http://localhost:5001/user'
        axios.get(path,{headers:{"Authorization":`Bearer ${localStorage.getItem("access_key")}`}})
             .then((info)=>{
                user_data.value.message=info.data.msg
                user_data.value.result=info.data.result
             })
    }
    
    const get_user_id=(id)=>{
        return user_data.value.result.filter((info)=>info["user_id"]==id)
    }
    
    const add_to_watchlist=()=>{
        if (!watchlist_check.value.pass){
            const path='http://localhost:5001/watchlist'
            const payload={"user_id":user_id,"book_id":book_id}
            axios.post(path,payload,{headers:{"Authorization":`Bearer ${localStorage.getItem("access_key")}`}})
            check_watchlist()
        }
    }
    const pay_book=(price)=>{
        const path='http://localhost:5001/status/buy'
        const payload={"user_id":user_id,"book_id":book_id,"price":price}
        axios.post(path,payload,{headers:{"Authorization":`Bearer ${localStorage.getItem("access_key")}`}})
        check_buy_status()
    }
    const request_book=(hrs,mins,sec)=>{
        if(hrs!==0 || mins!==0 || sec!==0){
            const path='http://localhost:5001/status/request'
            const payload={"user_id":user_id,"book_id":book_id,'expiry':`${hrs}:${mins}:${sec}`}
            console.log(payload)
            axios.post(path,payload,{headers:{"Authorization":`Bearer ${localStorage.getItem("access_key")}`}})
            check_request_status()
        }
        
    }
    const post_feedback=async(msg,score)=>{
        const path='http://localhost:5001/feedback'
        const payload={"user_id":user_id,"book_id":book_id,"feedback_message":msg,"feedback_score":score}
        await axios.post(path,payload,{headers:{"Authorization":`Bearer ${localStorage.getItem("access_key")}`}})
        get_feedbacks()
    }
</script>

<script>
    
    export default {
        data(){
            return {
                showPaymentModal:false,
                showReviewModal:false,
                showRequestModal:false,
                showEditFeedbackModal:false,
                editFeedbackModal:0,
            }
        },
        methods:{
            handlePaymentModal(condition,condiiton1,condition3){
                if(condition && condiiton1 && condition3){
                    this.showPaymentModal=!this.showPaymentModal
                }
            },
            handleReviewModal(){
                this.showReviewModal=!this.showReviewModal
            },
            handleRequestModal(condition,condition1,condiiton2,condition3,condition4){
                if(condition && condition1 && condiiton2 && condition3 && condition4){
                    this.showRequestModal=!this.showRequestModal
                }
                
            },
            handleEditFeedbackModal(feedback_id){
                this.editFeedbackModal=feedback_id
                this.showEditFeedbackModal=!this.showEditFeedbackModal
            },
            handle_redirect(id,id1,condition){

                if(condition){
                    this.$router.push({path:`/user/read/books/${id}/${id1}`})
                }
            }
        }
    }
</script>