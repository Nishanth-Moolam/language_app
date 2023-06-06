import { Injectable } from "@angular/core";
import { HttpClient } from '@angular/common/http';
import { BehaviorSubject, Observable, of, throwError } from 'rxjs';

@Injectable({
    providedIn: 'root'
})
export class HomeService { 

    constructor (private http: HttpClient) {}

}