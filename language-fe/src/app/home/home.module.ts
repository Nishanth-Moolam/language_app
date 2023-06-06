import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { HomeComponent } from './components/home/home.component';

import { MatTabsModule } from '@angular/material/tabs';
import { HomeService } from './home.service';
import { AboutComponent } from './components/about/about.component';
import { NewLessonComponent } from './components/new-lesson/new-lesson.component';
import { LessonListComponent } from './components/lesson-list/lesson-list.component';
import { GoogleSigninButtonModule, SocialLoginModule } from '@abacritt/angularx-social-login';
import { MatIconModule } from '@angular/material/icon';
import { MatMenuModule } from '@angular/material/menu';
import { MatButtonModule } from '@angular/material/button';


@NgModule({
  declarations: [
    HomeComponent,
    AboutComponent,
    NewLessonComponent,
    LessonListComponent,
  ],
  imports: [
    SocialLoginModule,
    GoogleSigninButtonModule,
    CommonModule,
    MatTabsModule,
    MatIconModule,
    MatMenuModule,
    MatButtonModule
  ],
  providers: [HomeService],
  exports: [
    HomeComponent, 
    AboutComponent, 
    NewLessonComponent, 
    LessonListComponent, 
    SocialLoginModule,
    GoogleSigninButtonModule
  ]
})
export class HomeModule { }
