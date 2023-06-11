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
import { MatSelectModule } from '@angular/material/select';
import { MatInputModule } from '@angular/material/input';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatButtonToggleModule } from '@angular/material/button-toggle';
import { ReactiveFormsModule } from '@angular/forms';
import { LessonComponent } from './components/lesson/lesson.component';
import { RouterModule } from '@angular/router';

@NgModule({
  declarations: [
    HomeComponent,
    AboutComponent,
    NewLessonComponent,
    LessonListComponent,
    LessonComponent,
  ],
  imports: [
    SocialLoginModule,
    GoogleSigninButtonModule,
    CommonModule,
    MatTabsModule,
    MatIconModule,
    MatMenuModule,
    MatButtonModule,
    MatSelectModule,
    MatInputModule,
    MatButtonToggleModule,
    MatFormFieldModule,
    ReactiveFormsModule,
    RouterModule,
  ],
  providers: [HomeService],
  exports: [
    HomeComponent,
    AboutComponent,
    NewLessonComponent,
    LessonListComponent,
    SocialLoginModule,
    GoogleSigninButtonModule,
  ],
})
export class HomeModule {}
