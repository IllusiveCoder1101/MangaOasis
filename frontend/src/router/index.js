import { createRouter, createWebHistory } from 'vue-router'
import landingView from '../views/landingView.vue';
import loginView from '@/views/loginView.vue'
import registerView from '@/views/registerView.vue';
import adminloginView from '@/views/adminloginView.vue';
import dashboardUserView from '@/views/dashboardUserView.vue';
import bookInfoView from '@/views/bookInfoView.vue';
import BooksView from '@/views/booksView.vue';
import booksReadView from '@/views/booksReadView.vue';
import adminDashboard from '@/views/adminDashboardView.vue';
import usersList from '@/views/usersListView.vue';
import booksList from '@/views/booksListView.vue';
import IssueList from '@/views/IssueListView.vue';
import IssuedList from '@/views/IssuedListView.vue';
import UserProfileView from '@/views/userProfileView.vue';
import BookPdfPreviewView from '@/views/bookPdfPreviewView.vue';
const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'landing',
      component: landingView
    },
    {
      path: '/user/login',
      name: 'login',
      component: loginView
    },
    {
      path: '/user/register',
      name: 'registration',
      component: registerView
    },
    {
      path: '/librarian/login',
      name: 'librarianlogin',
      component: adminloginView
    },
    {
      path: '/librarian/dashboard',
      name: 'librarianDashboard',
      component: adminDashboard,
      meta:{
        requiresAuth:true
      }
    },
    
    {
      path: '/librarian/books_list',
      name: 'librarianBooks',
      component: booksList,
      meta:{
        requiresAuth:true
      }
    },
    {
      path: '/librarian/users_list',
      name: 'librarianUsers',
      component: usersList,
      meta:{
        requiresAuth:true
      }
    },
    {
      path: '/librarian/issue_list',
      name: 'librarianIssue',
      component: IssueList,
      meta:{
        requiresAuth:true
      }
    },
    {
      path: '/librarian/issued_list',
      name: 'librarianIssued',
      component: IssuedList,
      meta:{
        requiresAuth:true
      }
    },
    {
      path: '/user/dashboard/:id',
      name: 'userDashboard',
      component: dashboardUserView,
      meta:{
        requiresAuth:true
      }
    },
    {
      path: '/user/profile/:id',
      name: 'userProfile',
      component: UserProfileView,
      meta:{
        requiresAuth:true
      }
    },
    {
      path: '/user/books/:id',
      name: 'userBooks',
      component: BooksView,
      meta:{
        requiresAuth:true
      }
    },
    {
      path: '/user/books/:id/:id1',
      name: 'userBooksInfo',
      component: bookInfoView,
      meta:{
        requiresAuth:true
      }
    },
    {
      path: '/user/read/books/:id/:id1',
      name: 'userBookRead',
      component: booksReadView,
      meta:{
        requiresAuth:true
      }
    },
    {
      path: '/user/preview/books/:id/:id1',
      name: 'userPdfPreview',
      component: BookPdfPreviewView,
      meta:{
        requiresAuth:true
      }
    }
  ]
})

router.beforeEach((to)=>{
  if(to.meta.requiresAuth && !localStorage.getItem("access_key")){
    return {name: 'login', query:{ redirect: to.fullPath }}
  }
})
export default router
