<template>
    <Loader/>
    <div class="dashboard_admin">
        <nav class="navbar" id="">
            <img src="../assets/images/manga-oasis logo.png" alt="logo" class="logo">
            <router-link to="/librarian/login"><button class="log_out"><vue-feather type="power" class="icon1" ></vue-feather></button></router-link>
        </nav>
        <section class="dashboard_section">
            <h1 class="dashboard_heading">Welcome To Dashboard</h1>
            <div class="status_container">
                <div class="status_box">
                    <vue-feather type="users" class="icon4"/>
                    <div class="status_desc">
                        <h3 class="status_title">TOTAL USERS</h3>
                        <h2 class="status_no">{{ user_data.result.length }}</h2>
                    </div>
                </div>
                <div class="status_box">
                    <vue-feather type="book" class="icon4"/>
                    <div class="status_desc">
                        <h3 class="status_title">TOTAL BOOKS</h3>
                        <h2 class="status_no">{{    book_data.result.length  }}</h2>
                    </div>
                </div>
                <div class="status_box">
                    <vue-feather type="dollar-sign" class="icon4"/>
                    <div class="status_desc">
                        <h3 class="status_title">TOTAL REVENUE</h3>
                        <h2 class="status_no">{{total_sales.res  }}</h2>
                    </div>
                </div>
            </div>
            <div >
                <div v-if="graph_info.data.labels.length>0" class="graph_section">
                    <Bar :data="graph_info.data" :options="graph_info.options" />
                </div>
                <div v-else class="error_state graph_section">
                    <p class="error_msg1">Graph Data not found.</p>
                </div>
            </div>
            <section class="other_status_section">
                <div class="status_section">
                   <div class="status_header">
                        <h3 class="status_heading1">Users</h3>
                        <router-link to="/librarian/users_list">
                            <button class="link_btn">View More</button>
                        </router-link>
                   </div>
                    <div v-if="user_data.result.length!=0" class="result_holder">
                        <div class="status_holder"  v-for="i in user_data.result.slice(0,4)" :key="i">
                            <div class="status_contain">
                                
                                <img :src='getimg(i["profile_pic"])' alt="profile_pic" class="profile_pic">
                                <div class="status_desc1">
                                    <p class="status_para">{{ i["user_name"]}}</p>
                                    <p class="status_para1">{{ i["email"]}}</p>
                                </div>
                            </div>
                                
                        </div>
                    </div>
                    <div v-else class="error_state">
                        <p class="error_msg1">No Users</p>
                    </div>
                    
                  
                   
                </div>
                <div class="status_section">
                   <div class="status_header">
                        <h3 class="status_heading1">Books</h3>
                        <router-link to="/librarian/books_list">
                            <button class="link_btn">View More</button>
                        </router-link>
                   </div>
                
                    <div v-if="book_data.result.length!=0" class="result_holder">
                        <div class="status_holder"  v-for="i in book_data.result.slice(0,4)" :key="i">
                            <div class="status_contain">
                            
                                <img :src="getBookImg(i['book_cover'])" alt="profile_pic" class="profile_pic">
                                <div class="status_desc1">
                                    <p class="status_para">{{ i["book_name"] }}</p>
                                    <p class="status_para1">{{ i["author_name"] }}</p>
                                </div>
                            </div>
                        </div>
                    </div>
                    <div v-else class="error_state">
                        <p class="error_msg1">No Books</p>
                    </div>
                  
                </div>
                <div class="status_section">
                   <div class="status_header">
                        <h3 class="status_heading1">Issue Requests</h3>
                        <router-link to="/librarian/issue_list">
                            <button class="link_btn">View More</button>
                        </router-link>
                   </div>
                   <div v-if="request_book_data.result.length!=0" class="result_holder">
                        
                        <div class="status_holder" v-for="i in request_book_data.result.slice(0,4)" :key="i">
                            <div class="status_contain">
                                <img :src="getBookImg(i['book_cover'])" alt="profile_pic" class="profile_pic">
                                <div class="status_desc1">
                                    <p class="status_para">{{ i["book_name"] }}</p>
                                    <p class="status_para1">{{ getNoOfBooks("request",i["book_id"]) }} Request</p>
                                </div>
                            </div>
                        </div>
                   </div>
                   <div v-else class="error_state">
                        <p class="error_msg1">No Requests Issued</p>
                   </div>
                </div>
                <div class="status_section">
                   <div class="status_header">
                        <h3 class="status_heading1"> Books Issued</h3>
                        <router-link to="/librarian/issued_list">
                            <button class="link_btn">View More</button>
                        </router-link>
                   </div>
                   <div v-if="issued_book_data.result.length>0" class="result_holder">
                        <div class="status_holder" v-for="i in issued_book_data.result.slice(0,4)" :key="i">
                            <div class="status_contain">
                                <img :src="getBookImg(i['book_cover'])" alt="profile_pic" class="profile_pic">
                                <div class="status_desc1">
                                    <p class="status_para">{{ i["book_name"] }}</p>
                                    <p class="status_para1">{{ getNoOfBooks("issue",i["book_id"]) }} Issued</p>
                                </div>
                            </div>
                        </div>
                        
                   </div>
                   <div v-else class="error_state">
                        <p class="error_msg1">No Books Issued</p>
                   </div>
                </div>
            </section>
        </section>
        <PageFooter/>
    </div>
    
</template>

<script setup lang="js">
    
    import PageFooter from '../components/pageFooter.vue'
    import axios from 'axios'
    import { onMounted,ref } from 'vue';
    import Loader from '@/components/loader.vue';
    import {
    Chart as ChartJS,
    Title,
    Tooltip,
    Legend,
    BarElement,
    CategoryScale,
    LinearScale
    } from 'chart.js'
    import { Bar } from 'vue-chartjs'

    ChartJS.register(CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend)
    ChartJS.defaults.backgroundColor = '#FCA17D';
    ChartJS.defaults.borderColor = '#F9DBBD';
    ChartJS.defaults.color = '#F9DBBD';

    onMounted(()=>{
        window.scrollTo(0,0)
        getData()
        
    })

    const user_data=ref({message:"",result:[]})
    const book_data=ref({message:"",result:[]})
    const issued_book_data=ref({message:"",result:[]})
    const request_book_data=ref({message:"",result:[]})
    const feedback_data=ref({message:"",result:[]})
    const graph_info=ref({data:{labels: [],datasets: [{ label:"",data: [] }]},options: {responsive: true}})
    const total_sales=ref({"res":0})
    const getData=async()=>{
        const path=`http://localhost:5001/user`
        await axios.get(path,{headers:{"Authorization":`Bearer ${localStorage.getItem("access_key")}`}})
            .then((info)=>{
                user_data.value.message=info.data.msg
                user_data.value.result=info.data.result
        })

        const path1="http://localhost:5001/book"
        await axios.get(path1,{headers:{"Authorization":`Bearer ${localStorage.getItem("access_key")}`}})
            .then((info)=>{
                book_data.value.message=info.data.msg
                book_data.value.result=info.data.result
        })

        const path2="http://localhost:5001/get_status"
        await axios.get(path2,{headers:{"Authorization":`Bearer ${localStorage.getItem("access_key")}`}})
            .then((info)=>{
                request_book_data.value.message=info.data.msg
                request_book_data.value.result=info.data.result.filter((data)=>data.status_type === "request").slice(0,4)
                issued_book_data.value.message=info.data.msg
                issued_book_data.value.result=info.data.result.filter((data)=>data.status_type==="accept" ).slice(0,4)       
                let tmp=info.data.result.filter((res)=>res["status_type"]=='buy')
                for(let i of tmp){
                    total_sales.value.res+=i['price']
                }
            })

        const path3="http://localhost:5001/feedback"
        await axios.get(path3,{headers:{"Authorization":`Bearer ${localStorage.getItem("access_key")}`}})
            .then((info)=>{
                feedback_data.value.message=info.data.msg
                feedback_data.value.result=info.data.result
            })
        get_graph_data()
    }
    const get_graph_data=()=>{
        const tmp={}
        for(let i of feedback_data.value.result){
            if( Object.keys(tmp).indexOf(getBookName(i["book_id"]))>=0){
                tmp[getBookName(i["book_id"])][0]+=i["feedback_score"]
                tmp[getBookName(i["book_id"])][1]+=1
            }
            else{
                tmp[getBookName(i["book_id"])]=[]
                tmp[getBookName(i["book_id"])].push(i["feedback_score"])
                tmp[getBookName(i["book_id"])].push(1)
            }
            
        }
        console.log(tmp)
        graph_info.value.data.labels=Object.keys(tmp)
        
        let l=[]
        for(let j of Object.values(tmp)){
            l.push(j[0]/j[1])
        }
        graph_info.value.data.datasets[0].data=l
        graph_info.value.data.datasets[0].label="Average Book Ratings"
    }
    const getimg=(pic)=>{
        return new URL(`../assets/images/${pic}`, import.meta.url).href
    }   
    const getBookImg=(pic)=>{
        return new URL(`../assets/manga_pics/${pic}`, import.meta.url).href
    }    
    const getBookName=(id)=>{
        return book_data.value.result.filter((data)=>data["book_id"]==id)[0]["book_name"]
    }
    const getNoOfBooks=(query,id)=>{
        if (query=="request"){
            return request_book_data.value.result.filter((info)=>info["book_id"]==id).length
        }
        else{
            return issued_book_data.value.result.filter((info)=>info["book_id"]==id).length
        }
    }
</script>

<script lang="js">
    export default {
    name: 'App',
    components: {
        Bar
    }}
</script>