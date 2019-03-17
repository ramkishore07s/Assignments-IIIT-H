# This file is auto-generated from the current state of the database. Instead
# of editing this file, please use the migrations feature of Active Record to
# incrementally modify your database, and then regenerate this schema definition.
#
# Note that this schema.rb definition is the authoritative source for your
# database schema. If you need to create the application database on another
# system, you should be using db:schema:load, not running all the migrations
# from scratch. The latter is a flawed and unsustainable approach (the more migrations
# you'll amass, the slower it'll run and the greater likelihood for issues).
#
# It's strongly recommended that you check this file into your version control system.

ActiveRecord::Schema.define(version: 20170920080710) do

  create_table "admins", force: :cascade do |t|
    t.datetime "created_at", null: false
    t.datetime "updated_at", null: false
    t.integer "user_id"
    t.index ["user_id"], name: "index_admins_on_user_id"
  end

  create_table "genres", force: :cascade do |t|
    t.string "parent"
    t.string "subtype"
    t.datetime "created_at", null: false
    t.datetime "updated_at", null: false
  end

  create_table "multiple_answers", force: :cascade do |t|
    t.string "question"
    t.string "option1"
    t.string "option2"
    t.string "option3"
    t.string "option4"
    t.boolean "answer1"
    t.boolean "answer2"
    t.boolean "answer3"
    t.boolean "answer4"
    t.datetime "created_at", null: false
    t.datetime "updated_at", null: false
    t.integer "genre_id"
    t.string "url"
    t.index ["genre_id"], name: "index_multiple_answers_on_genre_id"
  end

  create_table "multiple_choices", force: :cascade do |t|
    t.boolean "answer1"
    t.boolean "answer2"
    t.boolean "answer3"
    t.boolean "answer4"
    t.datetime "created_at", null: false
    t.datetime "updated_at", null: false
    t.integer "multiple_answer_id"
    t.integer "user_id"
    t.integer "touch_id"
    t.index ["multiple_answer_id"], name: "index_multiple_choices_on_multiple_answer_id"
    t.index ["touch_id"], name: "index_multiple_choices_on_touch_id"
    t.index ["user_id"], name: "index_multiple_choices_on_user_id"
  end

  create_table "single_answers", force: :cascade do |t|
    t.string "question"
    t.string "option1"
    t.string "option2"
    t.string "option3"
    t.string "option4"
    t.string "answer"
    t.datetime "created_at", null: false
    t.datetime "updated_at", null: false
    t.integer "genre_id"
    t.string "url"
    t.index ["genre_id"], name: "index_single_answers_on_genre_id"
  end

  create_table "single_choices", force: :cascade do |t|
    t.string "answer"
    t.datetime "created_at", null: false
    t.datetime "updated_at", null: false
    t.integer "touch_id"
    t.integer "single_answer_id"
    t.index ["single_answer_id"], name: "index_single_choices_on_single_answer_id"
    t.index ["touch_id"], name: "index_single_choices_on_touch_id"
  end

  create_table "touches", force: :cascade do |t|
    t.datetime "created_at", null: false
    t.datetime "updated_at", null: false
    t.integer "genre_id"
    t.integer "user_id"
    t.integer "score"
    t.index ["genre_id"], name: "index_touches_on_genre_id"
    t.index ["user_id"], name: "index_touches_on_user_id"
  end

  create_table "users", force: :cascade do |t|
    t.string "name"
    t.string "email"
    t.string "password"
    t.integer "score"
    t.datetime "created_at", null: false
    t.datetime "updated_at", null: false
    t.string "password_digest"
    t.index ["email"], name: "index_users_on_email", unique: true
  end

end
