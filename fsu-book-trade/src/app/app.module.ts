import { HeaderTemplateComponent } from './header-template/header-template.component';
import { HomeComponent } from './home/home.component';
import { RouterModule } from '@angular/router';
import { CUSTOM_ELEMENTS_SCHEMA, NgModule, Component } from '@angular/core';
import { ReactiveFormsModule } from '@angular/forms';
import { BrowserModule } from '@angular/platform-browser';
import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { FooterTemplateComponent } from './footer-template/footer-template.component';

@NgModule({
  declarations: [
    AppComponent,
    HomeComponent,
    HeaderTemplateComponent,
    FooterTemplateComponent,
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    ReactiveFormsModule,
    RouterModule.forRoot([
      { 
        path: '', 
        component: HomeComponent 
      },
    ])
  ],
  schemas: [CUSTOM_ELEMENTS_SCHEMA],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
