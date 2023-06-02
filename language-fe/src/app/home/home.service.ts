import { Injectable } from "@angular/core";
import { HttpClient } from '@angular/common/http';
import { Observable, of, throwError } from 'rxjs';

@Injectable({
    providedIn: 'root'
})
export class HomeService { 

    constructor (
        private http: HttpClient, 
        ) {}

}