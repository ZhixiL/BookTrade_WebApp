import { RestService } from './Services/rest.service';
import { HttpClientModule } from '@angular/common/http';
import { HeaderTemplateComponent } from './header-template/header-template.component';
import { FooterTemplateComponent } from './footer-template/footer-template.component';
import { HomeComponent } from './home/home.component';
import { RouterModule } from '@angular/router';
import { CUSTOM_ELEMENTS_SCHEMA, NgModule, Component } from '@angular/core';
import { ReactiveFormsModule } from '@angular/forms';
import { BrowserModule } from '@angular/platform-browser';
//import { FormsModule } from '@angular/forms';
import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { LoginComponent } from './login/login.component';
import { RegisterComponent } from './register/register.component';
import { BooklistComponent } from './booklist/booklist.component';
import { PostComponent } from './post/post.component';
import { NotfoundComponent } from './notfound/notfound.component';
import { ProfileComponent } from './profile/profile.component';

@NgModule({
  declarations: [
    //FormsModule,
    AppComponent,
    HomeComponent,
    HeaderTemplateComponent,
    FooterTemplateComponent,
    LoginComponent,
    RegisterComponent,
    BooklistComponent,
    PostComponent,
    NotfoundComponent,
    ProfileComponent,
  ],
  imports: [
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
        path: 'profile', 
        component: ProfileComponent 
      },
      { 
        path: 'post', 
        component: PostComponent 
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
        path: '**',
        component: NotfoundComponent
      },
    ])
  ],
  schemas: [CUSTOM_ELEMENTS_SCHEMA],
  providers: [RestService],
  bootstrap: [AppComponent]
})
export class AppModule { }
