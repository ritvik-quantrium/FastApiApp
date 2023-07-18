

from sqlalchemy import func
from .. import models,schemas,utils,oauth2
from fastapi import FastAPI,Response,status,HTTPException,Depends,APIRouter
from sqlalchemy.orm import Session
from ..database import SessionLocal, engine,get_db
from typing import List, Optional


router = APIRouter(
    prefix="/posts",
     tags = ["Posts"]
)

# @router.get("/",response_model=List[schemas.Post])
@router.get("/",response_model=List[schemas.PostOut])
def get_posts(db: Session = Depends(get_db),current_user = Depends(oauth2.get_current_user),limit: int =10 ,skip:int = 0,search:Optional[str]=""):

    # cursor.execute("""SELECT * FROM post""")
    # post = cursor.fetchall()
    # print(models.Post.title.contains(search))
    # print(db.query(models.Post).filter(models.Post.title.contains(search)))

    posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()


    # posts = db.query(models.Post).filter().all()
    # posts = db.query(models.Post).filter(models.Post.owner_id==current_user.id).all()
 
 

    # posts = db.query(models.Post)
    # print(posts)# will return query
 
 
    # results = db.query(models.Post , func.count(models.Votes.post_id).label("votes")).join(models.Votes,models.Votes.post_id == models.Post.id , isouter=True).group_by(models.Post.id).all()
    results = db.query(models.Post , func.count(models.Votes.post_id).label("votes")).join(models.Votes,models.Votes.post_id == models.Post.id , isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    # print(results[0][1])



    #this was not covered has to manually figure it out : If you dont write correct schema use this to figure out output
    # for i in range(len(results)):
    #     results[i] = {"post":results[i][0] , "votes":results[i][1]}




    return results
    # return posts




 



# @router.get("/{id}",response_model=schemas.Post)
@router.get("/{id}",response_model=schemas.PostOut)

def get_posts(id:int,db:Session = Depends(get_db),current_user = Depends(oauth2.get_current_user) ):
    #OLD Post retrieval without adding votes in database
    '''
    
    post = db.query(models.Post).filter(models.Post.id==id).first() #instead of looking everywhere just return first and stop
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND , detail=f"post with id :{id} was not found")

    # if post.owner_id != current_user.id:
    #     raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Not authorised")
    return post
    '''

    results = db.query(models.Post , func.count(models.Votes.post_id).label("votes")).join(models.Votes,models.Votes.post_id == models.Post.id , isouter=True).group_by(models.Post.id).filter(models.Post.id==id).first()

    if not results:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND , detail=f"post with id :{id} was not found")
    #we have removed the functionalty that the author of the post can only see the post
    # if results.Post.owner_id != current_user.id:
    #     raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Not authorised")

    return results

    # USING DIRECT POSTGRES CONNECTION
    '''

        cursor.execute("""SELECT * from post WHERE id = %s""" ,(str(id),))
        # post = cursor.fetchall()
        post = cursor.fetchone()
        if not post:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND , detail=f"post with id :{id} was not found")

        return {"post_detail":post}
    '''
    # USING SAMPLE DATABASE
    '''
    post = utitlty_for_post((int)(id))
    if not post:
        # response.status_code = 404
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND , detail=f"post with id :{id} was not found")
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"message"}

    # return {"post_detail":f"Here is post {id}"}
    return {"post_detail":post}'''


@router.post("/",status_code=status.HTTP_201_CREATED , response_model=schemas.Post)
def create_posts(post:schemas.PostCreate,db:Session = Depends(get_db) ,current_user = Depends(oauth2.get_current_user)):


    # new_post = models.Post(title = post.title , content = post.content , published = post.published)
    print("Detuch" )
    print(current_user)
    new_post = models.Post(owner_id = current_user.id , **post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post




    # cursor.execute("""INSERT INTO post(title, content, published) VALUES(%s, %s, %s) RETURNING *""",(post.title,post.content,post.published))
    # new_post = cursor.fetchone()
    # #commit changes 
    # conn.commit()


    # post_dict = post.dict()
    # post_dict["id"] = randrange(0,1000000)
    # Sample_Data.append(post_dict)
    # return {"data":new_post}



@router.delete("/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_posts(id:int,db:Session = Depends(get_db) ,current_user = Depends(oauth2.get_current_user )):



#  db.query(models.Post).filter(models.Post.id ==id is the query
    post_query = db.query(models.Post).filter(models.Post.id ==id)
    post = post_query.first()
    if post==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id = {id} was not found")
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Not authorised")

    post_query.delete(synchronize_session=False)
    db.commit()

    #USING direct postgres connection
    # cursor.execute("""DELETE FROM post WHERE id = %s returning *""",(str(id),))
    # deleted_post = cursor.fetchone()
    # conn.commit()

    # if deleted_post is None:
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id = {id} was not found")

    # return Response(status_code=status.HTTP_204_NO_CONTENT) # cant send back any data when STATUS CODE is 204
    #USING sample database
    # index = index_for_post(id)
    # if index is None:
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id :{id} was not found")

    # Sample_Data.pop(index)
    # return Response(status_code=status.HTTP_204_NO_CONTENT) # cant send back any data when STATUS CODE is 204




@router.put("/{id}",response_model=schemas.Post)
def update_post(id:int , updatedpost:schemas.PostCreate,db:Session = Depends(get_db) , current_user = Depends(oauth2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id==id)
    post = post_query.first()
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id = {id} was not found")
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Not authorised")

    post_query.update(updatedpost.dict() , synchronize_session=False)
    db.commit()
    return post_query.first()




    #Update Postgres using direct connection
    # cursor.execute("""UPDATE post SET title = %s ,content = %s , published = %s WHERE id = %s RETURNING *""",(post.title,post.content,post.published,str(id),))
    # updated_post = cursor.fetchone()
    # conn.commit()

    # if updated_post is None:
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id = {id} was not found")

    # return {'data':updated_post} 


    #Update Sample Data
    # index = index_for_post(id)
    # if index is None:
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id :{id} was not found")

    # cur_post = post.dict()
    # cur_post["id"] = id
    # Sample_Data[index] = cur_post
    # return {'data':cur_post} # cant send back any data when STATUS CODE is 204

















