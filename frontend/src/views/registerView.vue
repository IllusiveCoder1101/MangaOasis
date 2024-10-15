<template>

    <div class="login_page">
            <header class="login_header">
                <nav class="navbar" >
                    <img src="../assets/images/manga-oasis logo.png" alt="logo" class="logo">
                    
                </nav>
                
            </header>
            <main>
                <section class="login_form">
                    <h1 class="heading2">SIGN UP</h1>
                    <form action="" class="form">
                        <div class="form_container">
                            <div class="form_contain">
                                <vue-feather type="user" class="icon"></vue-feather>
                            <input type="text" v-model="user_data.username"  placeholder="Username" class="input_field">
                            </div>
                        </div>
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
                        <div class="form_container">
                            <div class="form_contain">
                                <vue-feather type="lock" class="icon"></vue-feather>
                                <input :type="(password_visible1.pass)?'text':'password'" v-model="user_data.confirm_password"  placeholder="Confirm Password" class="input_field">
                            </div>
                            <div class="side_icon">
                            <vue-feather :type="(password_visible1.pass)?'eye':'eye-off'" class="icon" :onclick="()=> password_visibility1()"></vue-feather>
                        </div>
                        </div>
                        <p v-if="error.res!=''" :class="(error.type=='error')?'error_msg':'success_msg'">{{ error.res }}</p>
                        <div class="form_container1">
                            <router-link to="/" class="link">Go back</router-link>
                            <router-link to="/user/login" class="link">Already have an Account?</router-link> 
                        </div>
                       <button type="submit" class="primary form_btn" @click.prevent="()=>handleSubmit()">SIGN UP</button> 
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
    })
    const password_visible=ref({pass:false})
    const password_visible1=ref({pass:false})
    const password_visibility=()=>{
        password_visible.value.pass=!password_visible.value.pass
    }
    const password_visibility1=()=>{
        password_visible1.value.pass=!password_visible1.value.pass
    }
</script>

<script>
    export default {
        data(){
            return {
                user_data:ref({
                    username:"",
                    email:"",
                    password:"",
                    confirm_password:""
                }),
                error:ref({"res":"","type":""})
            }
        },
        methods:{
            AddUser(payload){
                const path="http://localhost:5001/register_user"
                axios.post(path,payload)
                    .then((info)=>{
                        if(info.data.msg=="Registered Succesfully"){
                            this.error.res="Successfully Registered"
                            this.error.type="success"
                            setTimeout(()=>{
                                this.formReset()
                                this.handleRedirect()
                            },2000)
                        }
                    })
                    .catch(()=>{
                        this.error.res="User Already Exists"
                        this.error.type="error"
                    })
            },
            formReset(){
                this.user_data.username=""
                this.user_data.email=""
                this.user_data.password=""
                this.user_data.confirm_password=""
            },
            handleSubmit(){
                const payload={
                    user_name:this.user_data.username,
                    email:this.user_data.email,
                    password:this.user_data.password
                }
                if(payload.user_name.length>0 && payload.email.length>0 && payload.password.length>0 && this.user_data.password === this.user_data.confirm_password){
                    this.AddUser(payload)
                }
                else{
                    this.error.res="Invalid Data"
                    this.error.type="error"
                }
                
            },
            handleRedirect(){
                this.$router.push({path:"/user/login"})
            }
            
        }
        
        
    }
</script>