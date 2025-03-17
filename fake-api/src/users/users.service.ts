
import { Injectable } from '@nestjs/common';

// This should be a real class/interface representing a user entity
export type User = any;

@Injectable()
export class UsersService {
  private readonly exampleData = {
    firstName: 'John',
    lastName: 'Doe',
    phone: "+48 505 173 823",
    address: "Długa 46, Katowice",
    facebook: "Karol Frank",
    instagram: "Karol Frank",
    linkedin: "Karol Frank"
    }

  private readonly users = [
    {
      id: 1,
      email: 'superadmin',
      password: '1234',
      role: 0,
      ...this.exampleData
    },
    {
      id: 2,
      email: 'admin',
      password: '1234',
      role: 1,
      ...this.exampleData
    },
    {
      id: 3,
      email: 'user',
      password: '1234',
      role: 2,
      ...this.exampleData
    },
    {
      id: 4,
      email: '1',
      password: '1234',
      role: 1,
      ...this.exampleData
    },
    {
      id: 5,
      email: '2',
      password: '1234',
      role: 2,
      ...this.exampleData
    },
    {
      id: 6,
      email: '3',
      password: '1234',
      role: 2,
      ...this.exampleData
    },
  ];

  async findOne(email?: string|null, id?: number): Promise<User | undefined> {
    if(email) return this.users.find(user => user.email === email);
    else if(id) return this.users.find(user => user.id === id);
  }

  async findAll(): Promise<User | undefined> {
    return this.users;
  }
}
