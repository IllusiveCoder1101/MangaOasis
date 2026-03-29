<template>
    <Loader/>
    <div class="profile_page">
        <nav class="navbar">
            <img src="../assets/images/manga-oasis logo.png" alt="" class="logo">
            <router-link to="/user/login"><button class="log_out"><vue-feather type="power" class="icon1" ></vue-feather></button></router-link>
        </nav>
        <header class="profile_header">
            <div class="profile_desc1" :style="`background-image: url(${get_banner(user_data.result['profile_banner'])});`">
                <img :src="get_profile_pic(user_data.result['profile_pic'])" alt="profile_pic" class="profile_pic3">
                <div class="profile_contain1">
                    <h1 class="profile_header">{{ user_data.result["user_name"] }}</h1>
                    <p class="profile_para">{{ user_data.result["email"] }}</p>
                </div>
                <div class="edit_banner">
                    <vue-feather type="edit-2" class="icon" @click="()=>banner_Modal_Visibility()"></vue-feather>
                </div>
            </div>
        </header>
        <EditBannerModal v-if="banner_modal_visible" :close_func="banner_Modal_Visibility" :current_banner="user_data.result['profile_banner']" :handle_update_banner="update_banner"/>
        <main class="Profile_form_container">
            <form action="" class="profile_form">
                <div class="form_container">
                    <div class="form_contain">
                        <vue-feather type="user" class="icon"></vue-feather>
                        <input type="text" @input="new_data['username']=$event.target.value" :value="user_data.result['user_name']" placeholder="Email Address" class="input_field">
                    </div>
                </div>
                <div class="form_container">
                    <div class="form_contain">
                        <vue-feather type="mail" class="icon"></vue-feather>
                        <input type="email" @input="new_data['email']=$event.target.value" :value="user_data.result['email']" placeholder="Email Address" class="input_field">
                    </div>
                </div>
                <div class="form_container">
                    <div class="form_contain">
                        <vue-feather type="lock" class="icon"></vue-feather>
                        <input :type="(password_visible.pass)?'text':'password'" @input="new_data['password']=$event.target.value" :value="user_data.result['password']" placeholder="Email Address" class="input_field" >
                    </div>
                    <div class="side_icon">
                        <vue-feather :type="(password_visible.pass)?'eye':'eye-off'" class="icon" :onclick="()=> password_visibility()"></vue-feather>
                    </div>
                </div>
                <div class="form_container">
                    <div class="form_contain">
                        <vue-feather type="image" class="icon"></vue-feather>
                    <input type="file" ref="file"  class="input_field" @change="new_data['profile_pic']=read_img()">
                    </div>
                </div>
                <button type="submit" class="primary form_btn" @click.prevent="()=>update_user()">Update Account</button>
                <button type="submit" class="secondary form_btn" @click.prevent="()=>{remove_user();handle_redirect()}">Remove Account</button>
            </form>
        </main>
        <footer>
            <PageFooter/>
        </footer>
    </div>
</template>

<script setup>
    import PageFooter from '../components/pageFooter.vue'
    import EditBannerModal from '../components/editBannerModal.vue'
    import axios from 'axios'
    import { onMounted, ref } from 'vue';
    import { useRoute } from 'vue-router'
    import Loader from '../components/loader.vue';
    onMounted(()=>{
        window.scrollTo(0,0)
        get_user_data()
    })
    const route=useRoute()
    const user_id=route.params.id
    const user_data=ref({message:"",result:[]})
    const password_visible=ref({pass:false})
    const new_data=ref({"username":"","email":"","password":"","profile_pic":"","banner":""})
    const get_user_data=async()=>{
        const path1="http://localhost:5001/user"
        await axios.get(path1,{headers:{Authorization:`Bearer ${localStorage.getItem("access_key")}`}})
            .then((info)=>{
                let tmp=info.data.result
                user_data.value.message=info.data.msg
                user_data.value.result=tmp.filter((data)=>data["user_id"]==user_id)[0]
        })
    }
    const update_user=()=>{
        const path1=`http://localhost:5001/user/${user_id}`
        if (new_data.value.email.match(/^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)*$/)){
            const payload=new_data.value
            console.log(payload)
            axios.put(path1,payload,{headers:{Authorization:`Bearer ${localStorage.getItem("access_key")}`}})
            get_user_data()
        }
        
        
    }
    const update_banner=(new_banner)=>{
        new_data.value['banner']=new_banner
        const path1=`http://localhost:5001/user/${user_id}`
        const payload=new_data.value
        axios.put(path1,payload,{headers:{Authorization:`Bearer ${localStorage.getItem("access_key")}`}})
            .then((info)=>{
                console.log(info)
                get_user_data()
            })        
    }
    const remove_user=()=>{
        const path1=`http://localhost:5001/user/${user_id}`
        axios.delete(path1,{headers:{Authorization:`Bearer ${localStorage.getItem("access_key")}`}})
        
        
    }
    const get_banner=(pic)=>{
        return new URL(`../assets/images/${pic}`, import.meta.url).href
    }
    const get_profile_pic=(pic)=>{
        return new URL(`../assets/images/${pic}`, import.meta.url).href
    }
    const password_visibility=()=>{
        password_visible.value.pass=!password_visible.value.pass
    }
</script>

<script>
    export default {
        data(){
            return {
                banner_modal_visible:false
            }
        },
        methods:{
            read_img(){
                return this.$refs.file.files[0].name
            },
            handle_redirect(){
                this.$router.push({path:"/user/register"})
            },
            banner_Modal_Visibility(){
                this.banner_modal_visible=!this.banner_modal_visible
            }
        }
    }
</script>