import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { HomeService } from '../../home.service';
import { Word } from '../../models/word.interface';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';

@Component({
  selector: 'app-lesson',
  templateUrl: './lesson.component.html',
  styleUrls: ['./lesson.component.scss'],
})
export class LessonComponent implements OnInit {
  lesson: any;
  selectedWord: Word | null = null;
  form: FormGroup;
  view: string = 'words';

  constructor(
    private fb: FormBuilder,
    private route: ActivatedRoute,
    private homeService: HomeService
  ) {}

  ngOnInit(): void {
    this.getData();
    this.form = this.fb.group({
      translation: ['', Validators.required],
    });
  }

  getData(): void {
    this.homeService
      .getLesson(this.route.snapshot.paramMap.get('id'))
      .subscribe((lesson) => {
        this.lesson = lesson;
        // console.log(this.lesson);
      });
  }

  viewToggle(view: string): void {
    this.view = view;
    this.selectedWord = null;
  }

  backToLessons(): void {
    this.homeService.setTabIndex(2);
  }

  selectWord(word: Word | null): void {
    this.selectedWord = word;
  }

  changeKnowledgeLevel(word: Word, knowledge: number): void {
    this.homeService
      .changeKnowledge(word.id.$oid, knowledge)
      .subscribe((res) => {
        this.selectedWord ? (this.selectedWord.knowledge = knowledge) : null;
        this.getData();
      });
  }

  addTranslation(): void {
    const translation = this.form.value.translation;
    this.homeService
      .addTranslation(this.selectedWord?.id.$oid, translation)
      .subscribe((word) => {
        this.selectedWord = word;
        this.form.reset();
        this.getData();
      });
  }

  deleteTranslation(translation: string): void {
    this.homeService
      .deleteTranslation(this.selectedWord?.id.$oid, translation)
      .subscribe((word) => {
        this.selectedWord = word;
        this.getData();
      });
  }
}
