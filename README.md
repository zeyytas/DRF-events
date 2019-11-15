
<h1>Introduction</h1> 

DRF-events provides couple of filtering, grouping and sorting actions on Event database.

## Installation

First, start by closing the repository:

```
git clone https://github.com/zeyytas/DRF-events.git
```

Recommended to use `virtualenv` for development:

- Start by installing `virtualenv` if you don't have it
```
pip install virtualenv
```

- Create a virtual environment
```
virtualenv env
```

- Enable the virtual environment
```
source env/bin/activate
```

- Install the python dependencies on the virtual environment
```
pip install -r requirements.txt
```

## Action
<small>
   
GET         /api/v1? </small>

## Attributes

<small>
   
   - date_from and date_to

   ```e.g.   ?date_from=2017-05-17&date_to=2017-05-19```
   
   - name

   ```e.g.   ?name=facebook```


   - country

   ```e.g.   ?city=US,CA```
   
   - check-in count

   ```e.g.   ?checkin_count=66```
   
   - session count

   ```e.g.   ?session_count=16```
   
   - ticket count

   ```e.g.   ?ticket_count=456```
   
   - revenue

   ```e.g.   ?revenue=66```

   - sort_by </br>
   The default ordering is ascending. If you want to change the sort order to descending, append :desc to the field.

   ```e.g. ?sort_by=country:desc```

   - show </br>
   This attribute provides the field you want to be shown as a result
   
   ```e.g  ?show=revenue,date```
   
   - ticket price

   ```e.g.   ?show=tp```

   - group_by </br>
   This attribute provides broken down attribute with which field
   
   ```e.g  ?group_by=country```
</small>
