:::mermaid
erDiagram
    CUSTOMUSER {
        integerfield id
        emailfield email
        charfield password
        charfield username
        charfield nickname
        datetimefield created_at
        datetimefiled updated_at
        booleanfield is_staff
        Imagefield profiled_image
    }
    
    ACCOUNTBOOK_DATE {
        foreginkey user
        datefield date
        integerfield income 
        integerfield spending
        integerfield left_money
    }

    ACCOUNTBOOK_WRITE {
        datefield date
        charfield tag
        charfield res_income_spending
        integerfield money
        charfield content 
        
    }

    TAG {
        charfield tag
    }

    POST {
        integerfield id
        charfield title
        textfield content
        datetimefield created_at
        datetimefield updated_At
    }

    COMMENT {
        integerfield CUSTOMUSER_id
        charfield CUSTOMUSER_nickname
        integerfield POST_id

        charfield COMMENT_content
        datetimefield created_at
        datetimefield updated_At
    }

    CUSTOMUSER ||--o{ POST : "write"
    CUSTOMUSER ||--o{ COMMENT : "write"
    POST ||--o{ COMMENT : "post_comment"
    TAG }|--|{ ACCOUNTBOOK_WRITE : "tagging"
    CUSTOMUSER ||--o{ ACCOUNTBOOK_WRITE : "show"    
    ACCOUNTBOOK_WRITE }o--|| ACCOUNTBOOK_DATE : "bind"
    CUSTOMUSER ||--o{ACCOUNTBOOK_DATE : "write"
:::