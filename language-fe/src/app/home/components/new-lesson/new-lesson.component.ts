import { Component, OnInit, ViewEncapsulation } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { Lesson } from '../../models/lesson.interface';
import { HomeService } from '../../home.service';

@Component({
  selector: 'app-new-lesson',
  templateUrl: './new-lesson.component.html',
  styleUrls: ['./new-lesson.component.scss'],
  encapsulation: ViewEncapsulation.None,
})
export class NewLessonComponent implements OnInit {
  form: FormGroup;

  constructor(private fb: FormBuilder, private homeService: HomeService) {}

  ngOnInit(): void {
    this.form = this.fb.group({
      lessonName: ['', Validators.required],
      lessonLanguage: ['', Validators.required],
      nativeLanguage: ['', Validators.required],
      description: ['', Validators.required],
      lessonText: ['', Validators.required],
    });
  }

  onSubmit(): void {
    const lesson: Lesson = {
      language: this.form.value.lessonLanguage,
      description: this.form.value.description,
      title: this.form.value.lessonName,
      text: this.form.value.lessonText,
    };

    this.homeService.postLesson(lesson).subscribe((res) => {
      this.homeService.getLessonList().subscribe((lessons) => {
        this.homeService.setLessonList(lessons);
      });
    });

    // this.homeService.getLessonList().subscribe((lessons) => {
    //   this.homeService.setLessonList(lessons);
    // });

    // Reset form
    this.form.reset();

    // Move to lesson list tab
    this.homeService.setTabIndex(2);
  }
}
