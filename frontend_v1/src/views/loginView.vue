<template>

<div class="login_page">
        <header class="login_header">
            <nav class="navbar" >
                <img src="../assets/images/manga-oasis logo.png" alt="logo" class="logo">
                
            </nav>
            
        </header>
        <main>
            <section class="login_form">
                <h1 class="heading2">SIGN IN</h1>
                <form action="" class="form">
                    <div class="form_container">
                       <div class="form_contain">
                            <vue-feather type="mail" class="icon"></vue-feather>
                            <input type="email" v-model="user_data.email"  placeholder="Email Address" class="input_field">
                       </div>
                    </div>
                    <div class="form_container">
                        <div class="form_contain">
                            <vue-feather type="lock" class="icon"></vue-feather>
                            <input :type="(password_visible.pass)?'text':'password'" v-model="user_data.password"  placeholder="Password" class="input_field">
                        </div>
                        <div class="side_icon">
                            <vue-feather :type="(password_visible.pass)?'eye':'eye-off'" class="icon" :onclick="()=> password_visibility()"></vue-feather>
                        </div>
                    </div>
                    <p v-if="error.res!=''" :class="(error.type=='error')?'error_msg':'success_msg'">{{ error.res }}</p>
                    <div class="form_container1">
                        <router-link to="/" class="link">Go back</router-link>
                        <router-link to="/user/register" class="link"> Create an Account</router-link> 
                    </div>
                    <button type="submit" @click.prevent="()=>handleSubmit()" class="primary form_btn">SIGN IN</button>
                </form>
            </section>
            
        </main>
        <footer class="footer">
            <p class="footer_text">© 2024 Manga Oasis. All rights reserved.</p>
            <div class="icon_group">
                <vue-feather type="youtube" class="icon" ></vue-feather>
                <vue-feather type="facebook" class="icon"></vue-feather>
                <vue-feather type="twitter" class="icon"></vue-feather>
                <vue-feather type="twitch" class="icon"></vue-feather>
             
            </div>
        </footer>
    </div>
</template>
<script setup>
    import { onMounted } from 'vue';
    import axios from 'axios'
    import { ref } from 'vue';
    onMounted(()=>{
        window.scrollTo(0,0)
        localStorage.removeItem("access_key")
    })
    const password_visible=ref({pass:false})
    const password_visibility=()=>{
        password_visible.value.pass=!password_visible.value.pass
    }
</script>


<script>
    export default {
        data(){
            return {
                user_data:ref({           
                    email:"",
                    password:"",
                }),
                error:ref({"res":"","type":""})

            }
        },
        methods:{
            CheckUser(payload){
                const path="http://localhost:5001/login_user"
                axios.post(path,payload)
                    .then((info)=>{
                        console.log(info.data)
                        if (info.data.msg === "valid user"){
                            this.error.res="Successfully Logged In"
                            this.error.type="success"
                            localStorage.setItem("access_key",info.data.result[1])
                                
                            setTimeout(()=>{
                                this.formReset()
                                this.handleRedirect(info.data.result[0])
                            },1000)
                        }
                    }) 
                    .catch(()=>{
                        this.error.res="Invalid Email or Password"
                        this.error.type="error"
                    })               
            },
            formReset(){
                this.user_data.email=""
                this.user_data.password=""
          
            },
            handleSubmit(){

                const payload={
                    email:this.user_data.email,
                    password:this.user_data.password
                }
                if(payload.email.length>0 && payload.password.length>0){
                    this.CheckUser(payload)
                }
                else{
                    this.error.res="Missing Data"
                    this.error.type="error"
                }
            },
            handleRedirect(id){
                this.$router.push({path:`/user/dashboard/${id}`})
            }   
        }
    }
</script>