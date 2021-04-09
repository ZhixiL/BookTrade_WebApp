import { EventEmitterService } from './Services/event-emitter.service';
import { RestService } from './Services/rest.service';
import { HttpClientModule } from '@angular/common/http';
import { HeaderTemplateComponent } from './header-template/header-template.component';
import { FooterTemplateComponent } from './footer-template/footer-template.component';
import { HomeComponent } from './home/home.component';
import { RouterModule } from '@angular/router';
import { CUSTOM_ELEMENTS_SCHEMA, NgModule, Component } from '@angular/core';
import { ReactiveFormsModule } from '@angular/forms';
import { BrowserModule } from '@angular/platform-browser';
import { FormsModule } from '@angular/forms';
import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { LoginComponent } from './login/login.component';
import { RegisterComponent } from './register/register.component';
import { BooklistComponent } from './booklist/booklist.component';
import { PostComponent } from './post/post.component';
import { NotfoundComponent } from './notfound/notfound.component';
import { ProfileComponent } from './profile/profile.component';
import { BookDetailComponent } from './book-detail/book-detail.component';
import { PersonalProfileComponent } from './personal-profile/personal-profile.component';
import { AboutUsComponent } from './about-us/about-us.component';
import { BuyOrderComponent } from './buy-order/buy-order.component';
import { BuyListComponent } from './buy-list/buy-list.component';
import { CommonQuestionsComponent } from './common-questions/common-questions.component';

@NgModule({
  declarations: [
    AppComponent,
    HomeComponent,
    HeaderTemplateComponent,
    FooterTemplateComponent,
    LoginComponent,
    RegisterComponent,
    BooklistComponent,
    PostComponent,
    BuyOrderComponent,
    BuyListComponent,
    NotfoundComponent,
    ProfileComponent,
    BookDetailComponent,
    PersonalProfileComponent,
    AboutUsComponent,
    CommonQuestionsComponent,
  ],
  imports: [
    FormsModule,
    BrowserModule,
    AppRoutingModule,
    ReactiveFormsModule,
    BrowserModule,
    HttpClientModule,
    RouterModule.forRoot([
      { 
        path: '', 
        component: HomeComponent
      },
      { 
        path: 'login', 
        component: LoginComponent 
      },
     { 
       path: 'profile/:user', 
       component: ProfileComponent 
     },
     { 
      path: 'personal/:user', 
      component: PersonalProfileComponent 
      },
      { 
        path: 'post', 
        component: PostComponent 
      },
      { 
        path: 'booklist/:bookname', 
        component: BookDetailComponent 
      },
      { 
        path: 'booklist', 
        component: BooklistComponent 
      },
      {
        path: 'register',
        component: RegisterComponent
      },
      {
        path: 'commonlyaskedquestions',
        component: CommonQuestionsComponent
      },
      {
        path: 'aboutus',
        component: AboutUsComponent
      },
      {
	      path: 'buyorder',
        component: BuyOrderComponent
      },
      {
	      path: 'buylist',
        component: BuyListComponent
      },	
      {
        path: '**',
        component: NotfoundComponent
      },
    ])
  ],
  schemas: [CUSTOM_ELEMENTS_SCHEMA],
  providers: [
    RestService,
    EventEmitterService,
  ],
  bootstrap: [AppComponent]
})
export class AppModule { }
