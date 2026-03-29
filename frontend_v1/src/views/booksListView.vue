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
                        <h1 class="heading">Our Books</h1>
                        <div class="search_bar">
                            <vue-feather type="search" class="icon2" ></vue-feather>
                            <input type="text" name="" id="" @input="(event)=>changeSearchResult(event.target.value)" placeholder="Look for Books..." class="search_input">
                        </div>
                    </div>
                </header>   
                <div >
                    <div v-if="search_result.result.length>0" class="user_container">
                        <div class="book_card" v-for="i in search_result.result" :key="i">
                            <div class="user_card_header">
                                <div class="user_card_profile">
                                    <img :src="getBookCover(i.book_cover)" alt="manga_pic" class="profile_pic">
                                    <div class="user_card_desc">
                                        <p class="user_card_name">{{ i.book_name }}</p>
                                        <p class="user_card_email">{{ i.author_name }}</p>
                                    </div>
                                </div>
                                <button class="primary_btn2" @click="()=>optionsVisibility(i.book_id)" :key="i.book_id"><vue-feather type="more-horizontal" class="icon2"></vue-feather> </button>
                                <div class="options" v-if="optionsShowId == i.book_id && optionsShow">
                                    <button class="primary_btn01" @click="()=>addChapterVisibility()"><vue-feather type="plus"  class="icon2"/> Chapter</button>
                                    <AddChapterModal v-if="addChapterDialog" :close_func="addChapterVisibility" :handle_add_chapter="addChapter" :book_id="i.book_id" :error="add_chapter_error.msg"/>
                                    <button class="primary_btn01" @click="()=>editBookVisibility()"><vue-feather type="edit"  class="icon2"/> Book</button>
                                    <EditBookModal v-if="editBookDialog" :close_func="editBookVisibility" :get_book="getIdBook(i.book_id)"  :edit_book="editBook" :error="edit_book_error.msg"/>
                                    <button class="primary_btn01" @click="()=>removeBook(i.book_id)"><vue-feather type="trash" class="icon2"/> Book</button>
                                </div>
                
                            </div>
                            <div class="user_card_description">
                                <div v-if="i.chapters.length>0" >
                                    <div class="issue_card" v-for="j in i.chapters" :key="j">
                                        <div class="book_profile">
                                            <div class="user_card_desc">
                                                <p class="user_card_name1">Vol {{ j.volume_no }}</p>
                                                <p class="user_card_email1">Ch {{ j.chapter_no }}</p>
                                            </div>
                                            <p class="book_title">{{ j.chapter_name }}</p>
                                            
                                        </div>
                                        <div class="decision_btns">
                                            <EditChapterModal v-if="editChapterDialog==j['chapter_id']" :close_func="editChapterVisibility" :chapter_data1="j" :handle_chapter_edit="editChapter"  :error="edit_chapter_error.msg"/>
                                            <button class="btn_secondary" @click="()=>editChapterVisibility(j['chapter_id'])"><vue-feather type="edit"  class="icon5"/> </button>
                                            <button class="btn_secondary" @click="()=>removeChapter(j['chapter_id'])" ><vue-feather type="trash"  class="icon5"/> </button>
                                            
                                        </div>
                                    </div>
                                </div>
                                <div v-else class="error_state2">
                                    <p class="error_msg1">No Chapters</p>
                                </div>
                            </div>
            
                        </div>
                    </div>
                    <div v-else class="error_state">
                        <p class="error_msg1">No Books Found</p>
                    </div>
                </div>
                
                <AddBookModal   v-if="addBookDialog" :close_func="addBookVisibility" :handle_add_book="addBook"  :error="add_book_error.msg"/>
                <div class="new_container">
                    <button class="primary_btn02" @click="()=>addBookVisibility()"><vue-feather type="plus" class="icon2"></vue-feather> Book  </button>
                </div>
            </section>
        </div>
        <PageFooter/>
        <NotificationModal v-if="modal_display.display" :message="modal_display.message"/>
    </div>
                       
</template>



<script setup>
    import axios from 'axios';
    import { onMounted, ref } from 'vue';
    import Loader from '@/components/loader.vue';
    import AddChapterModal from '../components/addChapterModal.vue'
    import EditChapterModal from '../components/editChapterModal.vue'
    import EditBookModal from '../components/editBookModal.vue'
    import PageFooter from '../components/pageFooter.vue';
    import AddBookModal from '../components/addBookModal.vue'
    import NotificationModal from '../components/notificationModal.vue'
    
    
    onMounted(()=>{
        window.scrollTo(0,0)
        getBookData()
    })
    const book_data=ref({"message":"","result":[]})
    const search_result=ref({'result':[]})
    const add_chapter_error=ref({"msg":""})
    const add_book_error=ref({"msg":""})
    const edit_chapter_error=ref({"msg":""})
    const edit_book_error=ref({"msg":""})
    const modal_display=ref({"display":false,"message":""})
    const getBookData=async()=>{
        const path="http://localhost:5001/book"
        await axios.get(path,{headers:{Authorization:`Bearer ${localStorage.getItem("access_key")}`}})
            .then((data)=>{
                book_data.value.message=data.data.msg
                book_data.value.result=data.data.result
                search_result.value.result=data.data.result
            })
        
    }
    const changeSearchResult=(input)=>{
        search_result.value.result=book_data.value.result.filter((data)=>data['book_name'].toLowerCase().includes(input.toLowerCase()) || data['author_name'].toLowerCase().includes(input.toLowerCase()) )
    }
    const getBookCover=(p)=>{
        const pic=p
        return new URL(`../assets/manga_pics/${pic}`, import.meta.url).href
    }
    const getIdBook=(id)=>{
        return book_data.value.result.filter((info)=>info["book_id"] == id)[0]
    }
    const editBook=async(payload,id)=>{
        const path=`http://localhost:5001/book/${id}`
        await axios.put(path,payload,{headers:{"Authorization":`Bearer ${localStorage.getItem("access_key")}`}})
             .then(()=>{
                getBookData()
                modal_display.value.display=true
                modal_display.value.message="Book Edited Successfully!"
                setTimeout(()=>{
                    modal_display.value.display=false
                    modal_display.value.message=""
                },2000)
             })
             .catch(()=>{
                edit_book_error.value.msg="It Already Exists."
                setTimeout(()=>{
                    edit_book_error.value.msg=""
                },2000)
             })
    }
    const editChapter=async(payload,id)=>{
        const path=`http://localhost:5001/chapter/${id}`
        await axios.put(path,payload,{headers:{"Authorization":`Bearer ${localStorage.getItem("access_key")}`}})
             .then(()=>{
                getBookData()
                modal_display.value.display=true
                modal_display.value.message="Chapter Edited Successfully!"
                setTimeout(()=>{
                    modal_display.value.display=false
                    modal_display.value.message=""
                },2000)
             })
             .catch(()=>{
                edit_chapter_error.value.msg="It Already Exists."
                setTimeout(()=>{
                    edit_chapter_error.value.msg=""
                },2000)
             })
    }
    const removeBook=(id)=>{
        const path=`http://localhost:5001/book/${id}`
        axios.delete(path,{headers:{"Authorization":`Bearer ${localStorage.getItem("access_key")}`}})
        getBookData()
        modal_display.value.display=true
        modal_display.value.message="Book Removed Successfully!"
        setTimeout(()=>{
                    modal_display.value.display=false
                    modal_display.value.message=""
                },2000)
    }
    const removeChapter=(id)=>{
        const path=`http://localhost:5001/chapter/${id}`
        axios.delete(path,{headers:{"Authorization":`Bearer ${localStorage.getItem("access_key")}`}})
        getBookData()
        modal_display.value.display=true
        modal_display.value.message="Chapter Removed Successfully!"
        setTimeout(()=>{
                    modal_display.value.display=false
                    modal_display.value.message=""
                },2000)
    }
    const addBook=(payload)=>{
        const path='http://localhost:5001/book'
        axios.post(path,payload,{headers:{"Authorization":`Bearer ${localStorage.getItem("access_key")}`}})
             .then(()=>{
                getBookData()
                modal_display.value.display=true
                modal_display.value.message="Book Added Successfully!"
                setTimeout(()=>{
                    modal_display.value.display=false
                    modal_display.value.message=""
                },2000)
             })
             .catch(()=>{
                add_book_error.value.msg="It Already Exists."
                setTimeout(()=>{
                    add_book_error.value.msg=""
                },2000)
             })
    }
    const addChapter=(payload)=>{
        const path='http://localhost:5001/chapter'
        axios.post(path,payload,{headers:{"Authorization":`Bearer ${localStorage.getItem("access_key")}`}})
            .then(()=>{
                getBookData()
                add_chapter_error.value.msg=""
                modal_display.value.display=true
                modal_display.value.message="Chapter Added Successfully!"
                setTimeout(()=>{
                    modal_display.value.display=false
                    modal_display.value.message=""
                },2000)
            }) 
            .catch((error)=>{
                add_chapter_error.value.msg="It Already Exists."
                setTimeout(()=>{
                    add_chapter_error.value.msg=""
                },2000)
             })
        
    }
</script>

<script>
    export default {
        data(){
            return {
                addBookDialog:false,
                optionsShowId:'',
                optionsShow:false,
                addChapterDialog:false,
                editChapterDialog:'',
                editBookDialog:false,
            }
        },
        methods:{
            addBookVisibility(){
                this.addBookDialog=!this.addBookDialog
            },
            optionsVisibility(id){
                this.optionsShowId=id
                this.optionsShow=!this.optionsShow
            },
            addChapterVisibility(){
                this.addChapterDialog=!this.addChapterDialog
            },
            editChapterVisibility(id){
                this.editChapterDialog=id
            },
            editBookVisibility(){
                this.editBookDialog=!this.editBookDialog
            },
        }
    }
</script>